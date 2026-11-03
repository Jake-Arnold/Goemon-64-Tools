#include "virtual_clock.h"
#include <cassert>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <thread>
#include <vector>

int main() {
    VirtualClock clock(1000);
    assert(clock.speed_percent()==100 && clock.now_us(1000)==0);
    assert(clock.now_us(2000)==1000 && clock.host_deadline_us(3000,2000)==4000);
    clock.set_speed(200,2000);
    assert(clock.now_us(2000)==1000 && clock.now_us(2500)==2000);
    assert(clock.host_deadline_us(3000,2500)==3000);
    clock.set_speed(125,2500);
    assert(clock.now_us(2500)==2000 && clock.host_deadline_us(3001,2500)==3301);
    assert(clock.now_us(3301)==3001 && clock.host_deadline_us(1000,3301)==3301);
    clock.set_speed(100,3301);
    assert(clock.now_us(3301)==3001 && clock.now_us(3401)==3101);
    bool bad=false; try { clock.set_speed(0,3401); } catch (const std::invalid_argument&) { bad=true; }
    assert(bad && clock.speed_percent()==100 && clock.now_us(3401)==3101);
    bad=false; try { clock.now_us(3300); } catch (const std::invalid_argument&) { bad=true; }
    assert(bad);
    bad=false; try { clock.host_deadline_us(std::numeric_limits<std::int64_t>::max(),3401); } catch (const std::out_of_range&) { bad=true; }
    assert(bad);
    VirtualClock fractional(0); fractional.set_speed(125,0); fractional.set_speed(150,1);
    assert(fractional.now_us(1)==1 && fractional.now_us(2)==2 && fractional.host_deadline_us(3,2)==3);
    VirtualClock shared(0);
    std::vector<std::thread> workers;
    for (int i=0;i<4;i++) workers.emplace_back([&shared] {
        for (int j=0;j<1000;j++) { shared.set_speed(j % 2 ? 100 : 400, 0); assert(shared.now_us(0)==0); }
    });
    for (auto &worker : workers) worker.join();
    return 0;
}
