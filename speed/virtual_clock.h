#ifndef GOEMON_VIRTUAL_CLOCK_H
#define GOEMON_VIRTUAL_CLOCK_H

#include <cstdint>
#include <limits>
#include <mutex>
#include <stdexcept>

// A deterministic, thread-safe timing primitive for a future host integration.
// Times are monotonic microseconds; speed is an integer percentage (100..400).
// The caller must wake and reschedule timer/VI waiters after a speed change.
class VirtualClock {
public:
    explicit VirtualClock(std::int64_t host_us) : host_epoch_us_(host_us) {
        if (host_us < 0) throw std::invalid_argument("negative host time");
    }

    std::int64_t now_us(std::int64_t host_us) const {
        std::lock_guard<std::mutex> lock(mutex_);
        return scaled_now(host_us) / 100;
    }

    int speed_percent() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return speed_percent_;
    }

    void set_speed(int percent, std::int64_t host_us) {
        if (percent < 100 || percent > 400 || percent % 25 != 0)
            throw std::invalid_argument("speed must be 100..400 in 25 percent steps");
        std::lock_guard<std::mutex> lock(mutex_);
        virtual_epoch_hundredths_ = scaled_now(host_us);
        host_epoch_us_ = host_us;
        speed_percent_ = percent;
    }

    // Return the earliest host microsecond at which target guest time is reached.
    // Call again after each speed change; previously calculated deadlines expire.
    std::int64_t host_deadline_us(std::int64_t target_guest_us, std::int64_t host_us) const {
        if (target_guest_us < 0 || target_guest_us > max_value() / 100)
            throw std::out_of_range("guest deadline outside supported range");
        std::lock_guard<std::mutex> lock(mutex_);
        const auto current = scaled_now(host_us);
        const auto target = target_guest_us * 100;
        if (target <= current) return host_us;
        const auto remaining = target - current;
        const auto delay = remaining / speed_percent_ + (remaining % speed_percent_ != 0);
        if (host_us > max_value() - delay) throw std::overflow_error("host deadline overflow");
        return host_us + delay;
    }

private:
    static constexpr std::int64_t max_value() { return std::numeric_limits<std::int64_t>::max(); }
    std::int64_t scaled_now(std::int64_t host_us) const {
        if (host_us < host_epoch_us_) throw std::invalid_argument("host clock moved backwards");
        const auto delta = host_us - host_epoch_us_;
        if (delta > (max_value() - virtual_epoch_hundredths_) / speed_percent_)
            throw std::overflow_error("virtual clock overflow");
        return virtual_epoch_hundredths_ + delta * speed_percent_;
    }
    mutable std::mutex mutex_;
    std::int64_t host_epoch_us_;
    std::int64_t virtual_epoch_hundredths_ = 0;
    int speed_percent_ = 100;
};
#endif
