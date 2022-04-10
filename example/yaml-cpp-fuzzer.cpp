#include <string>
#include <stdint.h>
#include <iostream>
#include "yaml-cpp/yaml.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
   try {
       if (Size > 0) {
       YAML::Node doc = YAML::Load(std::string(reinterpret_cast<const char *>(Data), Size));
       }
   } catch (const YAML::Exception& e) {
   } catch (const std::exception& e) { }
 return 0;  // Non-zero return values are reserved for future use.
}
