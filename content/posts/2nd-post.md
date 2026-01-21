---
title: "C++ 상속(Inheritance)으로 확장하는 물리 엔진: 다양한 물리 객체 구현하기"
date: 2026-01-22
categories: [Programming, Physics]
tags: [C++, OOP, Inheritance, PhysicsEngine, Simulation]
math: true
comments: true
draft: false
summary: "기본 Particle 클래스를 상속받아 중력, 공기 저항, 반발력 등 서로 다른 물리적 성질을 가진 객체들을 효율적으로 설계하는 방법을 알아봅니다."
---

## 1. 상속(Inheritance): 물리 엔진의 확장성 확보

자! 지난 포스팅에서 만든 `Particle` 클래스는 기초 물리 법칙만 수행했지요? 하지만 실제 환경에는 서로 다른 특징을 가진 객체들이 있습니다! 예를 들어 불꽃(Spark), 연기(Smoke), 단단한 공(Ball) 등이 있죠!!

이때 각 객체마다 코드를 새로 만들지 말고!!! 공통 기능(위치, 속도 계산)은 **부모 클래스**에 두고 고유한 특징은 **자식 클래스**에서 정의하는 것이 상속의 핵심입니다!!

---
## 2. 클래스 계층 구조 설계

상속을 이용하면 아래와 같은 계층 구조를 가질 수 있습니다.
### 3. C++ 상속 구현 코드

부모 클래스의 `update` 메서드를 가상 함수(virtual)로 선언 그리고 자식 클래스에서 각 물리 법칙에 맞게 재정의(Override)하는 것이 포인트입니다!! 쉽죠?

```cpp
#include <iostream>
#include <vector>

// 기본 Particle 클래스 (부모)
class Particle {
protected: // 자식 클래스에서 접근 가능하도록 protected 설정
    Vector2D position;
    Vector2D velocity;
    double mass;

public:
    Particle(Vector2D pos, double m) : position(pos), velocity({0,0}), mass(m) {}
    
    // 가상 소멸자 필수
    virtual ~Particle() {}

    // 가상 함수: 자식에서 다르게 구현할 수 있음
    virtual void update(double deltaTime) {
        // 기본 가속도 법칙 (기본값은 등속도 운동)
        position += velocity * deltaTime;
    }

    void setVelocity(Vector2D v) { velocity = v; }
};

// 상속 1: 중력의 영향을 받는 입자
class GravityParticle : public Particle {
private:
    const double G = -9.8;

public:
    GravityParticle(Vector2D pos, double m) : Particle(pos, m) {}

    // 오버라이딩: 중력 가속도 적용
    void update(double deltaTime) override {
        velocity.y += G * deltaTime; 
        Particle::update(deltaTime); // 부모의 위치 업데이트 로직 호출
    }
};

// 상속 2: 공기 저항을 받는 입자 (감쇠 적용)
class SmokeParticle : public Particle {
private:
    double drag; // 저항 계수

public:
    SmokeParticle(Vector2D pos, double m, double d) : Particle(pos, m), drag(d) {}

    void update(double deltaTime) override {
        velocity = velocity * drag; // 매 프레임 속도 감소
        Particle::update(deltaTime);
    }
};
```
### 4. 다형성(Polymorphism)의 활용
상속의 진짜 마법은 다형성에서 나타납니다. 부모 타입의 포인터 배열 하나로 서로 다른 성질의 입자들을 한꺼번에 관리할 수 있습니다.

```C++

int main() {
    std::vector<Particle*> world;

    world.push_back(new GravityParticle({0, 100}, 1.0));
    world.push_back(new SmokeParticle({0, 0}, 0.5, 0.95));

    for (int i = 0; i < 100; ++i) {
        for (auto p : world) {
            p->update(0.1); // 각 객체의 실제 타입에 맞는 update가 호출됨!
        }
    }

    // 메모리 해제
    for (auto p : world) delete p;
    return 0;
}
```

## 5. 경제 모델로의 응용: 다양한 경제 주체
이 설계 방식은 경제 시뮬레이션에서도 똑같이 적용됩니다.

Base Class: EconomicAgent (자산, 소비 로직)

Derived Class 1: Consumer (소비 성향이 높은 주체)

Derived Class 2: Investor (자산 증식 로직이 강화된 주체)

이처럼 상속을 이용하면 복잡한 시스템을 매우 단순하고 명쾌하게 설계할 수 있습니다.

## 💡 오늘의 OOP 핵심 요약
Protected: 자식 클래스에게만 데이터 접근을 허용합니다.

Virtual Function: 실행 시점(Runtime)에 어떤 메서드를 실행할지 결정하는 다형성의 기초입니다.

Override: 부모의 기능을 내 입맛에 맞게 수정합니다.

다음 시간에는 객체 생성의 복잡함을 해결해주는 **팩토리 패턴(Factory Pattern)**에 대해 알아보겠습니다!