// Windows process-scoped control channel; caller opens Local\\Goemon64Speed_<PID>.
// The channel uses the process-default DACL. The
// channel reports applied rate, and disappears when the host process exits.
#ifdef _WIN32
struct GoemonSpeedChannel {
    volatile LONG magic, version, pid, requested, applied, guest_millis;
};
static void goemon_start_speed_channel() {
    wchar_t name[80];
    swprintf_s(name, L"Local\\Goemon64Speed_%lu", GetCurrentProcessId());
    HANDLE mapping = CreateFileMappingW(INVALID_HANDLE_VALUE, nullptr, PAGE_READWRITE,
                                        0, sizeof(GoemonSpeedChannel), name);
    if (!mapping) return;
    if (GetLastError() == ERROR_ALREADY_EXISTS) { CloseHandle(mapping); return; }
    auto *channel = static_cast<GoemonSpeedChannel *>(MapViewOfFile(mapping, FILE_MAP_ALL_ACCESS, 0, 0, sizeof(GoemonSpeedChannel)));
    if (!channel) { CloseHandle(mapping); return; }
    const LONG initial = goemon_clock.multiplier();
    InterlockedExchange(&channel->version, 2);
    InterlockedExchange(&channel->pid, static_cast<LONG>(GetCurrentProcessId()));
    InterlockedExchange(&channel->requested, initial);
    InterlockedExchange(&channel->applied, initial);
    InterlockedExchange(&channel->guest_millis, static_cast<LONG>(static_cast<ULONG>(goemon_clock.now_us() / 1000)));
    InterlockedExchange(&channel->magic, 0x47363453);
    std::thread([channel, mapping]() {
        // Mapping and handle intentionally live until process termination.
        (void)mapping;
        for (;;) {
            LONG requested = InterlockedCompareExchange(&channel->requested, 0, 0);
            LONG applied = InterlockedCompareExchange(&channel->applied, 0, 0);
            if (requested >= 1 && requested <= 4 && requested != applied) {
                goemon_clock.set_multiplier(static_cast<int>(requested));
                timer_context.action_queue.enqueue(SpeedChangedAction{});
                InterlockedExchange(&channel->applied, requested);
            }
            InterlockedExchange(&channel->guest_millis, static_cast<LONG>(static_cast<ULONG>(goemon_clock.now_us() / 1000)));
            Sleep(20);
        }
    }).detach();
}
#else
static void goemon_start_speed_channel() {}
#endif
