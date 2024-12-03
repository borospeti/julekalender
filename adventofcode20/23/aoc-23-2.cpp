#include <list>
#include <algorithm>
#include <iostream>

class CrabCups {

public:
    // const static int N      =  9;
    // const static int TURNS  = 100;
    const static int N      =  1000000;
    const static int TURNS  = 10000000;
    const static int PICKED =        3;

    // CrabCups() : cups_ { 3, 8, 9, 1, 2, 5, 4, 6, 7 } {
    CrabCups() : cups_ { 9, 2, 5, 1, 7, 6, 8, 3, 4 } {
        for (int i = 10; i <= N; ++i) {
            cups_.push_back(i);
        }
    }

    int pred(int n) const {
        return n > 1 ? n - 1 : N;
    }

    void turn() {
        int current = cups_.front();
        cups_.pop_front();
        std::list<int> pick;
        auto next = cups_.begin();
        for (int i = 0; i < PICKED; ++i) ++next;
        pick.splice(pick.begin(), cups_, cups_.begin(), next);
        int dest = pred(current);
        while (std::find(pick.begin(), pick.end(), dest) != pick.end()) dest = pred(dest);
        // std::cout << current << " -> " << dest << std::endl;
        auto pos = std::find(cups_.begin(), cups_.end(), dest);
        ++pos;
        cups_.splice(pos, pick);
        cups_.push_back(current);
    }

    void play(int n = TURNS) {
        int one_p = n / 10000;
        for (int i = 0; i < n; ++i) {
            if (one_p > 0 && i % one_p == 0) {
                std::cout << "done:" << (100.0 * i) / n << "%" << "  current=" << cups_.front() << std::endl;
            }
            turn();
        }
    }

    long result(void) {
        auto pos = std::find(cups_.begin(), cups_.end(), 1);
        ++pos;
        if (pos == cups_.end()) pos = cups_.begin();
        long res = *pos;
        ++pos;
        if (pos == cups_.end()) pos = cups_.begin();
        res *= *pos;
        return res;
    }

    void dump(void) {
        std::cout << "cups:";
        for (auto& cup : cups_) std::cout << " " << cup;
        std::cout << std::endl;
    }

private:
    std::list<int> cups_;
};


int main(int argc, char **argv) {

    CrabCups game;

    game.play();

    std::cout << "result=" << game.result() << std::endl;
}
