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
#elif defined(__linux__)
// Native Linux counterpart of the v2 process-scoped Windows IPC.
// Uses POSIX shm with user-only permissions; process exits unlink its name.
// The stock (unpatched) recomp has no speed channel.
#include <atomic>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <thread>
#include <unistd.h>
struct GoemonSpeedChannel {
    std::int32_t magic, version, pid, requested, applied, guest_millis;
};
static_assert(sizeof(GoemonSpeedChannel) == 24, "Goemon speed channel ABI changed");
static char goemon_speed_shm_name[80] = {};
static void goemon_unlink_speed_channel() {
    if (goemon_speed_shm_name[0]) shm_unlink(goemon_speed_shm_name);
}
static void goemon_start_speed_channel() {
    const long pid = static_cast<long>(getpid());
    std::snprintf(goemon_speed_shm_name, sizeof(goemon_speed_shm_name),
                  "/goemon64speed_%ld", pid);
    const int fd = shm_open(goemon_speed_shm_name, O_RDWR | O_CREAT | O_EXCL | O_CLOEXEC, 0600);
    if (fd < 0) return;  // Never take over a stale or foreign channel.
    if (ftruncate(fd, sizeof(GoemonSpeedChannel)) != 0) {
        close(fd);
        goemon_unlink_speed_channel();
        return;
    }
    void *mapped = mmap(nullptr, sizeof(GoemonSpeedChannel), PROT_READ | PROT_WRITE,
                        MAP_SHARED, fd, 0);
    close(fd);
    if (mapped == MAP_FAILED) {
        goemon_unlink_speed_channel();
        return;
    }
    auto *channel = static_cast<GoemonSpeedChannel *>(mapped);
    const auto initial = static_cast<std::int32_t>(goemon_clock.multiplier());
    __atomic_store_n(&channel->version, 2, __ATOMIC_RELEASE);
    __atomic_store_n(&channel->pid, static_cast<std::int32_t>(pid), __ATOMIC_RELEASE);
    __atomic_store_n(&channel->requested, initial, __ATOMIC_RELEASE);
    __atomic_store_n(&channel->applied, initial, __ATOMIC_RELEASE);
    __atomic_store_n(&channel->guest_millis,
                     static_cast<std::int32_t>(static_cast<std::uint32_t>(goemon_clock.now_us() / 1000)),
                     __ATOMIC_RELEASE);
    __atomic_store_n(&channel->magic, 0x47363453, __ATOMIC_RELEASE);
    std::atexit(goemon_unlink_speed_channel);
    std::thread([channel]() {
        for (;;) {
            const auto requested = __atomic_load_n(&channel->requested, __ATOMIC_ACQUIRE);
            const auto applied = __atomic_load_n(&channel->applied, __ATOMIC_ACQUIRE);
            if (requested >= 1 && requested <= 4 && requested != applied) {
                goemon_clock.set_multiplier(static_cast<int>(requested));
                timer_context.action_queue.enqueue(SpeedChangedAction{});
                __atomic_store_n(&channel->applied, requested, __ATOMIC_RELEASE);
            }
            __atomic_store_n(&channel->guest_millis,
                             static_cast<std::int32_t>(static_cast<std::uint32_t>(goemon_clock.now_us() / 1000)),
                             __ATOMIC_RELEASE);
            std::this_thread::sleep_for(std::chrono::milliseconds(20));
        }
    }).detach();
}
#else
static void goemon_start_speed_channel() {}
#endif
