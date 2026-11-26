/* Goemon scripted player-one input plugin, Mupen64Plus input API 2.1.
 * Build against the installed Mupen64Plus SDK, not copied ABI structs. */
#include <stdatomic.h>
#include <stdint.h>
#include <m64p_plugin.h>

static _Atomic uint32_t input_word;
static _Atomic uint32_t poll_count;
static int started;

EXPORT m64p_error CALL PluginStartup(m64p_dynlib_handle core, void *ctx,
                                    void (*log)(void *, int, const char *)) {
    (void)core; (void)ctx; (void)log;
    if (started) return M64ERR_ALREADY_INIT;
    started = 1; atomic_store(&input_word, 0); atomic_store(&poll_count, 0);
    return M64ERR_SUCCESS;
}
EXPORT m64p_error CALL PluginShutdown(void) {
    if (!started) return M64ERR_NOT_INIT;
    started = 0; atomic_store(&input_word, 0); atomic_store(&poll_count, 0);
    return M64ERR_SUCCESS;
}
EXPORT m64p_error CALL PluginGetVersion(m64p_plugin_type *type, int *version,
    int *api, const char **name, int *caps) {
    if (type) *type = M64PLUGIN_INPUT;
    if (version) *version = 0x010000;
    if (api) *api = 0x020100;
    if (name) *name = "Goemon scripted input";
    if (caps) *caps = 0;
    return M64ERR_SUCCESS;
}
/* Private frontend extension, not a network API. N64 wire button mask. */
EXPORT int CALL GoemonSetInput(unsigned buttons, int x, int y) {
    if (!started || buttons > 0xffff || (buttons & 0xc0) || x < -80 || x > 80 || y < -80 || y > 80) return 0;
    atomic_store(&input_word, (buttons << 16) | ((uint32_t)(uint8_t)x << 8) | (uint8_t)y);
    return 1;
}
EXPORT unsigned CALL GoemonTakePolls(void) { return atomic_exchange(&poll_count, 0); }
EXPORT void CALL InitiateControllers(CONTROL_INFO info) {
    for (int i=0; i<4; ++i) {
        info.Controls[i].Present = i == 0;
        info.Controls[i].RawData = 0;
        info.Controls[i].Plugin = PLUGIN_NONE;
        info.Controls[i].Type = CONT_TYPE_STANDARD;
    }
}
EXPORT void CALL GetKeys(int controller, BUTTONS *keys) {
    keys->Value = 0;
    if (controller != 0) return;
    uint32_t w = atomic_load(&input_word);
    unsigned b = w >> 16;
    keys->A_BUTTON=!!(b&0x8000); keys->B_BUTTON=!!(b&0x4000);
    keys->Z_TRIG=!!(b&0x2000); keys->START_BUTTON=!!(b&0x1000);
    keys->U_DPAD=!!(b&0x0800); keys->D_DPAD=!!(b&0x0400);
    keys->L_DPAD=!!(b&0x0200); keys->R_DPAD=!!(b&0x0100);
    keys->L_TRIG=!!(b&0x20); keys->R_TRIG=!!(b&0x10);
    keys->U_CBUTTON=!!(b&8); keys->D_CBUTTON=!!(b&4);
    keys->L_CBUTTON=!!(b&2); keys->R_CBUTTON=!!(b&1);
    keys->X_AXIS=(int8_t)(w>>8); keys->Y_AXIS=(int8_t)w;
    atomic_fetch_add(&poll_count, 1);
}
EXPORT int CALL RomOpen(void) { return 1; }
EXPORT void CALL RomClosed(void) { atomic_store(&input_word,0); atomic_store(&poll_count,0); }
EXPORT void CALL ControllerCommand(int c, unsigned char *cmd) { (void)c; (void)cmd; }
EXPORT void CALL ReadController(int c, unsigned char *cmd) { (void)c; (void)cmd; }
EXPORT void CALL SDL_KeyDown(int mod, int key) { (void)mod; (void)key; }
EXPORT void CALL SDL_KeyUp(int mod, int key) { (void)mod; (void)key; }
EXPORT void CALL RenderCallback(void) {}
