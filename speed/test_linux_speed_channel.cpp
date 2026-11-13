// Synthetic Linux runtime speed-channel host; no game sources or ROM required.
#include <atomic>
#include <chrono>
#include <cstdint>
#include <thread>

struct SpeedChangedAction {};
struct GoemonClockMock {
    std::atomic<int> rate{1};
    int multiplier() const { return rate.load(); }
    std::int64_t now_us() const { return 4000000; }
    void set_multiplier(int value) { rate.store(value); }
} goemon_clock;
struct WakeQueueMock {
    std::atomic<int> count{0};
    void enqueue(SpeedChangedAction) { count.fetch_add(1); }
};
struct TimerContextMock {
    WakeQueueMock action_queue;
} timer_context;

#include "runtime_channel.inc"

int main() {
    goemon_start_speed_channel();
    for (int i = 0; i < 250; ++i) {
        if (goemon_clock.multiplier() == 4 && timer_context.action_queue.count.load() > 0) {
            std::this_thread::sleep_for(std::chrono::milliseconds(250));
            return 0;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }
    return 2;
}
