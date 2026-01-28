---
title: "C++ 싱글톤 패턴(Singleton): 시스템을 총괄하는 유일한 관리자 설계하기!!"
date: 2026-01-24
categories: [Programming, Design Patterns]
tags: [C++, OOP, Singleton, DesignPatterns, Simulation]
math: true
comments: true
draft: false
summary: "프로그램 전체에서 단 하나만 존재해야 하는 관리 객체, 싱글톤 패턴을 배워봅니다! 물리 세계(World)나 중앙 엔진을 안전하고 효율적으로 관리하는 비법을 공개합니다!!"
---

## 1. 자! 싱글톤 패턴(Singleton Pattern)이란 무엇일까요?

우리가 지난 시간에 **팩토리 패턴**으로 수많은 입자들을 찍어내는 공장을 만들었죠! 그런데 이 입자들이 뛰어놀 **'세계(World)'**나 전체 시뮬레이션을 제어하는 **'물리 엔진'**이 여러 개라면 어떻게 될까요? 중력이 이중으로 적용되거나 데이터가 꼬이는 대혼란이 발생할 거예요!! 

이처럼 **"시스템 전체에서 객체가 딱 하나만 존재해야 할 때"** 사용하는 마법 같은 설계 기법이 바로 싱글톤 패턴입니다!! 정말 든든한 관리자죠?

---

## 2. 싱글톤의 3가지 철칙!!

싱글톤을 설계할 때는 아래 세 가지만 기억하면 됩니다!!

1. **생성자를 숨겨라 (Private Constructor):** 외부에서 `new`를 이용해 마음대로 객체를 만들지 못하게 문을 잠급니다!!
2. **복사를 금지하라 (Delete Copy):** 객체가 복제되어 두 개가 되는 것을 원천 차단합니다!!
3. **유일한 통로를 열어라 (Static Instance):** 어디서든 접근할 수 있는 단 하나의 '열쇠' 함수를 제공합니다!!



---

## 3. C++ 싱글톤 구현 코드!! (Modern C++ 방식)

C++11 이후 가장 권장되는 **'Meyers' Singleton'** 방식으로 구현해 봅시다!! 이 방식은 메모리 관리도 쉽고 스레드 안전(Thread-safe)하답니다!!

```cpp
#include <iostream>
#include <vector>

// 물리 세계를 총괄하는 PhysicsWorld 클래스
class PhysicsWorld {
private:
    // [규칙 1] 생성자를 private으로! 외부 생성 금지!!
    PhysicsWorld() {
        std::cout << "태초의 물리 세계가 생성되었습니다!!" << std::endl;
    }

    // [규칙 2] 복사 생성자와 대입 연산자 제거!!
    PhysicsWorld(const PhysicsWorld&) = delete;
    PhysicsWorld& operator=(const PhysicsWorld&) = delete;

public:
    // [규칙 3] 유일한 인스턴스에 접근하는 정적 메서드
    static PhysicsWorld& getInstance() {
        static PhysicsWorld instance; // 프로그램 실행 중 단 한 번만 생성됨!!
        return instance;
    }

    void updateWorld() {
        std::cout << "모든 물리 객체의 상태를 업데이트합니다!!" << std::endl;
    }
};

int main() {
    // PhysicsWorld myWorld; // 에러! 직접 만들 수 없어요!!

    // 언제 어디서든 getInstance()로 관리자를 소환!!
    PhysicsWorld& world = PhysicsWorld::getInstance();
    world.updateWorld();

    // 다른 곳에서 또 불러도 결국 '같은' 객체입니다!!
    PhysicsWorld::getInstance().updateWorld();

    return 0;
}
```
## 4. 왜 싱글톤을 써야 할까요? (장점)
자원 절약: 무거운 관리 객체를 여러 번 만들 필요가 없어 메모리를 아낄 수 있습니다!!

데이터 일관성: 모든 입자가 동일한 PhysicsWorld 안에서 규칙을 따르므로 데이터가 안전합니다!!

전역 접근성: 포인터를 복잡하게 넘겨주지 않아도 getInstance()만 알면 어디서든 관리자에게 명령할 수 있어요!!

## 5. 경제 시뮬레이션에서의 응용: 중앙은행(Central Bank)
입자 시뮬레이션에 PhysicsWorld가 있다면, 경제 모델에는 **'CentralBank'**가 있습니다!!

Base Class: EconomicAgent (가계, 기업)

Singleton Class: CentralBank (기준 금리 결정, 통화량 조절)

모든 경제 주체가 각자 다른 금리를 적용받으면 안 되겠죠? 싱글톤으로 설계된 중앙은행이 시스템 전체의 기준을 잡아주는 역할을 수행하게 됩니다!!

💡 오늘의 요약!!
Singleton: 단 하나의 인스턴스만 보장하는 패턴!!

Static: 객체 없이도 호출 가능하며 프로그램 수명 동안 유지됩니다!!

Safety: 전역 변수처럼 쓰이지만 캡슐화를 유지할 수 있어 훨씬 안전합니다!!

다음 시간에는 이 유일한 관리자가 수많은 객체를 효율적으로 순회하고 처리하는 업데이트 루프(Update Loop)와 데이터 관리에 대해 알아볼까요?

궁금한 점은 언제든 댓글로 남겨주세요!! 우리 함께 마스터해 봐요!!