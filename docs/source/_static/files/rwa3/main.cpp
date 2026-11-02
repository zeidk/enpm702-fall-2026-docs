/**
 * @file main.cpp
 * @author Firstname Lastname (your_email@umd.edu)
 * @brief RWA3: the demonstration program of your project.
 * @version 0.1
 * @date 2026-11-17
 *
 * @copyright Copyright (c) 2026
 *
 * @details This file compiles as given and prints the four section headers.
 * Fill each section with your own classes: replace each TODO with the code it
 * describes. Keep the sections and their headers in this order: they are how
 * your work is found when it is graded. Each section prints at least one line
 * of its own after its header, so the output shows what it demonstrates.
 */

#include <iostream>
#include <memory>
#include <stdexcept>
#include <vector>

// TODO: include your own headers, one per class.

int main() {
  // ===== 1: Inheritance and polymorphism =====
  std::cout << "[1] Inheritance and polymorphism\n";
  // TODO: create a std::vector of smart pointers to your base class, holding
  //       at least one object of each derived class.
  // TODO: in one loop over the vector, call one virtual method on each object.
  //       Each object must print its own line: the line shows which derived
  //       method ran.

  // ===== 2: Aggregation =====
  std::cout << "[2] Aggregation\n";
  // TODO: create a part with std::make_shared, and add it to a whole that
  //       holds it as a std::shared_ptr.
  // TODO: print the part's use_count() while the whole holds it.
  // TODO: destroy the whole (let its block end, or reset it), then use the
  //       part again and print its use_count(): the part outlives the whole.

  // ===== 3: Composition =====
  std::cout << "[3] Composition\n";
  // TODO: in a block of its own, create a whole that owns its parts (a
  //       std::unique_ptr member, or a member held by value).
  // TODO: at the end of the block, the whole is destroyed with its parts. Each
  //       destructor prints one line, so the output shows the order.

  // ===== 4: A broken rule =====
  std::cout << "[4] A broken rule\n";
  // TODO: in a try block, create an object with a value that one of your
  //       requirements forbids. Catch the std::invalid_argument it throws and
  //       print its message.
}
