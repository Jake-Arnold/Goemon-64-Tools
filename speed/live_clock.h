#ifndef GOEMON_LIVE_CLOCK_H
#define GOEMON_LIVE_CLOCK_H

#ifdef GOEMON_HOST_RUNTIME
#include "goemon_virtual_clock.h"
#include "goemon_startup_multiplier.h"
#else
#include "virtual_clock.h"
#include "startup_multiplier.h"
#endif
#include <chrono>
#include <cstdint>
#include <mutex>
#include <stdexcept>

// One clock domain for VI and N64 timers. The caller must wake timer waiters
// whenever set_multiplier succeeds. steady_clock supplies monotonic host time.
class GoemonLiveClock {
public:
    GoemonLiveClock() : origin_(std::chrono::steady_clock::now()), clock_(0) {
        clock_.set_speed(static_cast<int>(goemon_speed::startup_multiplier()) * 100, 0);
    }
    std::int64_t now_us() {
        std::lock_guard<std::mutex> lock(gate_);
        return clock_.now_us(host_us());
    }
    std::int64_t delay_until_us(std::int64_t guest_us) {
        std::lock_guard<std::mutex> lock(gate_);
        const auto now = host_us();
        return clock_.host_deadline_us(guest_us, now) - now;
    }
    int multiplier() {
        std::lock_guard<std::mutex> lock(gate_);
        return clock_.speed_percent() / 100;
    }
    void set_multiplier(int value) {
        if (value < 1 || value > 4) throw std::invalid_argument("unsupported speed");
        std::lock_guard<std::mutex> lock(gate_);
        clock_.set_speed(value * 100, host_us());
    }
private:
    std::int64_t host_us() const {
        return std::chrono::duration_cast<std::chrono::microseconds>(
            std::chrono::steady_clock::now() - origin_).count();
    }
    std::chrono::steady_clock::time_point origin_;
    VirtualClock clock_;
    std::mutex gate_;
};
#endif
