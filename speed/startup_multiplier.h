#ifndef GOEMON_STARTUP_MULTIPLIER_H
#define GOEMON_STARTUP_MULTIPLIER_H
#include <cstdint>
#include <cstdlib>

// Fixed for one process lifetime so VI and timer rates cannot change out of sync.
// Invalid or absent values use normal speed.
namespace goemon_speed {
inline std::uint32_t parse_startup_multiplier(const char *value) {
    if (!value || value[0] < '1' || value[0] > '4' || value[1] != '\0') return 1;
    return static_cast<std::uint32_t>(value[0] - '0');
}
inline std::uint32_t startup_multiplier() {
    return parse_startup_multiplier(std::getenv("GOEMON_SPEED_MULTIPLIER"));
}
}
#endif
