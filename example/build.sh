set -eux
cd "$(dirname "${BASH_SOURCE[0]}")"
rm -rf build
mkdir build
pushd build
CXX=clang++ CXXFLAGS="-g -fsanitize=fuzzer-no-link,address" cmake ../../yaml-cpp
make -j
popd
clang++ yaml-cpp-fuzzer.cpp -o yaml-cpp-fuzzer -fsanitize=fuzzer,address -Lbuild -lyaml-cpp -I../yaml-cpp/include
