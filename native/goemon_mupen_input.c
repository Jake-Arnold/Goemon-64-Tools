/* Goemon scripted and optional stock SDL player-one input, Mupen64Plus API 2.1.
 * Build against the installed Mupen64Plus SDK, not copied ABI structs. */
#include <stdatomic.h>
#include <stdint.h>
#include <stddef.h>
#include <dlfcn.h>
#include <m64p_plugin.h>

static _Atomic uint32_t input_word;
static _Atomic uint32_t poll_count;
static int started;
static _Atomic int physical_mode;
/* Optional local stock SDL plugin. It owns joystick discovery and configuration;
 * scripted mode never calls its GetKeys. No external input injection service. */
static void *provider;
static m64p_error (*provider_start)(m64p_dynlib_handle, void *, void (*)(void *, int, const char *));
static m64p_error (*provider_shutdown)(void);
static void (*provider_initiate)(CONTROL_INFO);
static void (*provider_keys)(int, BUTTONS *);
static int (*provider_open)(void);
static void (*provider_close)(void);
static void (*provider_key_down)(int, int);
static void (*provider_key_up)(int, int);

EXPORT int CALL GoemonConfigurePhysical(const char *path) {
    if (started || provider || !path || !*path) return 0;
    void *handle = dlopen(path, RTLD_NOW | RTLD_LOCAL);
    if (!handle) return 0;
    /* Reject our own bridge (and recursive bridges). */
    if (dlsym(handle, "GoemonSetInput")) { dlclose(handle); return 0; }
    m64p_error (*version)(m64p_plugin_type *, int *, int *, const char **, int *) = dlsym(handle, "PluginGetVersion");
    m64p_plugin_type kind; int api = 0;
    if (!version || version(&kind, NULL, &api, NULL, NULL) != M64ERR_SUCCESS ||
            kind != M64PLUGIN_INPUT || api != 0x020100) { dlclose(handle); return 0; }
    provider_start = dlsym(handle, "PluginStartup");
    provider_shutdown = dlsym(handle, "PluginShutdown");
    provider_initiate = dlsym(handle, "InitiateControllers");
    provider_keys = dlsym(handle, "GetKeys");
    provider_open = dlsym(handle, "RomOpen");
    provider_close = dlsym(handle, "RomClosed");
    provider_key_down = dlsym(handle, "SDL_KeyDown");
    provider_key_up = dlsym(handle, "SDL_KeyUp");
    if (!provider_start || !provider_shutdown || !provider_initiate || !provider_keys ||
            !provider_open || !provider_close || !provider_key_down || !provider_key_up) {
        dlclose(handle); return 0;
    }
    provider = handle;
    return 1;
}

EXPORT int CALL GoemonUsePhysical(void) {
    if (!started || !provider) return 0;
    atomic_store(&input_word, 0);
    atomic_store(&physical_mode, 1);
    return 1;
}

EXPORT m64p_error CALL PluginStartup(m64p_dynlib_handle core, void *ctx,
                                    void (*log)(void *, int, const char *)) {
    if (started) return M64ERR_ALREADY_INIT;
    if (provider) {
        m64p_error result = provider_start(core, ctx, log);
        if (result != M64ERR_SUCCESS) { dlclose(provider); provider = NULL; return result; }
    }
    started = 1; atomic_store(&input_word, 0); atomic_store(&poll_count, 0);
    atomic_store(&physical_mode, 0);
    return M64ERR_SUCCESS;
}
EXPORT m64p_error CALL PluginShutdown(void) {
    if (!started) return M64ERR_NOT_INIT;
    started = 0; atomic_store(&input_word, 0); atomic_store(&poll_count, 0);
    atomic_store(&physical_mode, 0);
    if (provider) {
        m64p_error result = provider_shutdown();
        dlclose(provider); provider = NULL; return result;
    }
    return M64ERR_SUCCESS;
}
EXPORT m64p_error CALL PluginGetVersion(m64p_plugin_type *type, int *version,
    int *api, const char **name, int *caps) {
    if (type) *type = M64PLUGIN_INPUT;
    if (version) *version = 0x010100;
    if (api) *api = 0x020100;
    if (name) *name = "Goemon scripted input";
    if (caps) *caps = 0;
    return M64ERR_SUCCESS;
}
/* Private frontend extension, not a network API. N64 wire button mask. */
EXPORT int CALL GoemonSetInput(unsigned buttons, int x, int y) {
    if (!started || buttons > 0xffff || (buttons & 0xc0) || x < -80 || x > 80 || y < -80 || y > 80) return 0;
    atomic_store(&input_word, (buttons << 16) | ((uint32_t)(uint8_t)x << 8) | (uint8_t)y);
    atomic_store(&physical_mode, 0);
    return 1;
}
EXPORT unsigned CALL GoemonTakePolls(void) { return atomic_exchange(&poll_count, 0); }
EXPORT void CALL InitiateControllers(CONTROL_INFO info) {
    if (provider) provider_initiate(info);
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
    if (provider && atomic_load(&physical_mode)) {
        provider_keys(controller, keys);
        atomic_fetch_add(&poll_count, 1);
        return;
    }
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
EXPORT int CALL RomOpen(void) { return provider ? provider_open() : 1; }
EXPORT void CALL RomClosed(void) { atomic_store(&input_word,0); atomic_store(&poll_count,0); atomic_store(&physical_mode,0); if (provider) provider_close(); }
EXPORT void CALL ControllerCommand(int c, unsigned char *cmd) { (void)c; (void)cmd; }
EXPORT void CALL ReadController(int c, unsigned char *cmd) { (void)c; (void)cmd; }
EXPORT void CALL SDL_KeyDown(int mod, int key) { if (provider) provider_key_down(mod, key); }
EXPORT void CALL SDL_KeyUp(int mod, int key) { if (provider) provider_key_up(mod, key); }
EXPORT void CALL RenderCallback(void) {}
