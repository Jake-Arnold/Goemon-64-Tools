#include "live_clock.h"
#include <cassert>
#include <chrono>
#include <thread>
#include <vector>
#include <cstdlib>
int main() {
    GoemonLiveClock clock;
    assert(clock.multiplier() == static_cast<int>(goemon_speed::startup_multiplier()));
    clock.set_multiplier(1);
    auto before=clock.now_us();
    std::this_thread::sleep_for(std::chrono::milliseconds(30));
    auto one=clock.now_us();
    assert(one >= before + 10000);
    auto pending=one+200000;
    auto first_wait=clock.delay_until_us(pending);
    clock.set_multiplier(2);
    auto switch_time=clock.now_us();
    auto second_wait=clock.delay_until_us(pending);
    assert(switch_time >= one && second_wait < first_wait && second_wait > 0);
    std::this_thread::sleep_for(std::chrono::milliseconds(30));
    auto two=clock.now_us();
    assert(two > switch_time + 35000);
    clock.set_multiplier(1);
    assert(clock.now_us() >= two);
    bool bad=false; try { clock.set_multiplier(0); } catch (const std::invalid_argument&) { bad=true; }
    assert(bad && clock.multiplier()==1);
    std::vector<std::thread> workers;
    for (int i=0;i<4;i++) workers.emplace_back([&clock,i] {
        std::int64_t last=0;
        for (int j=0;j<500;j++) {
            if (i==0) clock.set_multiplier((j%2)+1);
            auto now=clock.now_us(); assert(now>=last); last=now;
        }
    });
    for (auto &worker:workers) worker.join();
    return 0;
}
