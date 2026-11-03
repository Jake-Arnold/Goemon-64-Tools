#include "startup_multiplier.h"
#include <cassert>
int main() {
    assert(goemon_speed::parse_startup_multiplier(nullptr)==1);
    assert(goemon_speed::parse_startup_multiplier("")==1);
    assert(goemon_speed::parse_startup_multiplier("1")==1);
    assert(goemon_speed::parse_startup_multiplier("2")==2);
    assert(goemon_speed::parse_startup_multiplier("3")==3);
    assert(goemon_speed::parse_startup_multiplier("4")==4);
    assert(goemon_speed::parse_startup_multiplier("0")==1);
    assert(goemon_speed::parse_startup_multiplier("5")==1);
    assert(goemon_speed::parse_startup_multiplier("2x")==1);
    assert(goemon_speed::parse_startup_multiplier(" 2")==1);
    assert(goemon_speed::parse_startup_multiplier("-1")==1);
    const char *expected = std::getenv("GOEMON_EXPECT_SPEED");
    if (expected) assert(goemon_speed::startup_multiplier()==goemon_speed::parse_startup_multiplier(expected));
    return 0;
}
