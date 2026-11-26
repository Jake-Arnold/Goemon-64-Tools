"""Managed Mupen64Plus 2.6.0 slot operations at neutral frame boundaries."""
from __future__ import annotations

LOAD, SAVE, SET_SLOT = 10, 11, 12
LOAD_COMPLETE, SAVE_COMPLETE = 10, 11
PAUSED, ADVANCE = 3, 20
NEUTRAL = dict(buttons=0, x=0, y=0)


def state_complete(inspector, parameter, value):
    with inspector.cv:
        if inspector.state_job_expected == parameter:
            inspector.state_job_result = value == 1
            inspector.cv.notify_all()


def run_state_job(inspector, operation, slot, confirm=False):
    """Queue a job, let core interrupts process it, and require completion + pause.

    The stock API processes state jobs on emulation interrupts, not immediately
    at CoreDoCommand. A bounded neutral advance is required; exact zero-frame
    save/restore is not promised. An unresolved job quarantines the session.
    """
    if operation not in ('save_state', 'load_state') or type(slot) is not int or not 0 <= slot <= 9:
        raise ValueError('Choose a savestate slot from 0 to 9')
    if getattr(inspector.core, 'core_version', None) != 0x020600:
        raise RuntimeError('Managed savestates require Mupen64Plus core 2.6.0')
    load = operation == 'load_state'
    with inspector.cv:
        if inspector.state != PAUSED or inspector.recording or inspector.stepping or inspector.state_job_expected is not None:
            raise RuntimeError('Pause and stop recording before a savestate operation')
        if load and inspector.rows and confirm is not True:
            raise RuntimeError('Export or recover the old trace before loading; confirmation required')
        inspector.state_job_result = None
        inspector.state_job_notice = ''
        inspector.set_input(NEUTRAL)
        if load:
            # Never reuse live pointers or mix a restored state with an old trace.
            inspector.rows = []; inspector.last = None; inspector.watches = []
            inspector.player_base = None; inspector.player_text = None
            inspector.watch_errors = {}; inspector.error = ''
            inspector.unlock_result = None
        inspector.state_job_expected = LOAD_COMPLETE if load else SAVE_COMPLETE
    completed = False
    try:
        inspector.core.queue_state(LOAD if load else SAVE, slot)
        for _ in range(4):
            before = inspector.serial
            inspector.core.cmd(ADVANCE)
            inspector.wait(lambda: inspector.serial > before and inspector.state == PAUSED, timeout=5)
            with inspector.cv:
                inspector.cv.wait_for(lambda: inspector.state_job_result is not None or inspector.finished, timeout=1)
                if inspector.state_job_result is not None:
                    completed = True
                    break
                if inspector.finished:
                    raise RuntimeError('Core stopped during savestate operation')
        if not completed:
            raise RuntimeError('Savestate completion not acknowledged; stop and relaunch the session')
        if not inspector.state_job_result:
            raise RuntimeError(f'Savestate slot {slot} operation failed (check slot/file)')
        inspector.state_job_notice = (f'Loaded slot {slot}; reapply or relocate watches.' if load else f'Saved slot {slot} at a neutral core boundary.')
    finally:
        # If queued work is not acknowledged, do not allow another command to
        # race a delayed save/load. Only status and stop are then accepted.
        if completed:
            with inspector.cv:
                inspector.state_job_expected = None
