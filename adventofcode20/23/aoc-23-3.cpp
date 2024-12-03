#include <array>
#include <vector>
#include <iostream>

class CrabCups {

public:
    CrabCups(int size, const std::vector<int>& start)
        : size_(size)
        , current_(start[0])
        , cups_(size + 1)
    {
        int pred = size;
        for (auto& s : start) {
            cups_[pred] = s;
            pred = s;
        }
        cups_[pred] = current_;  // in case size is the same as start size
        for (int i = start.size() + 1; i <= size; ++i) {
            cups_[pred] = i;
            pred = i;
        }
    }

    int pred(int n) const {
        return n > 1 ? n - 1 : size_;
    }

    void turn() {
        int p1 = cups_[current_];
        int p2 = cups_[p1];
        int p3 = cups_[p2];
        int dest = pred(current_);
        while (dest == p1 || dest == p2 || dest == p3) dest = pred(dest);
        int next = cups_[dest];

        cups_[current_] = cups_[p3];
        cups_[dest] = p1;
        cups_[p3] = next;

        current_ = cups_[current_];
    }

    void play(int n) {
        for (int i = 0; i < n; ++i) {
            turn();
        }
    }

    long result(void) {
        long p1 = cups_[1];
        return p1 * cups_[p1];
    }

    void dump(void) {
        std::cout << "cups:";
        int n = current_;
        do {
            std::cout << " " << n;
            n = cups_[n];
        } while (n > 0 && n != current_);
        std::cout << std::endl;
    }

private:
    int size_;
    int current_;
    std::vector<int> cups_;
};


int main(int argc, char **argv) {

    std::vector<int> TEST  { 3, 8, 9, 1, 2, 5, 4, 6, 7 };
    std::vector<int> START { 9, 2, 5, 1, 7, 6, 8, 3, 4 };

    CrabCups game { 1000000, START };
    game.play(10000000);

    std::cout << "result = " << game.result() << std::endl;
}
