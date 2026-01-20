---
title: "C++ OOP로 구현하는 물리 시뮬레이션: 객체지향으로 설계하는 입자(Particle) 엔진"
date: 2026-01-20
categories: [Programming, Physics]
tags: [C++, OOP, Simulation, PhysicsEngine]
math: true
comments: true
draft: false
summary: "C++의 객체지향 원칙을 활용하여 물리 엔진의 기초가 되는 입자 시스템을 설계해 봅니다. 캡슐화와 연산자 오버로딩을 통해 유지보수가 용이한 코드를 작성하는 방법을 다룹니다."
---

## 1. 왜 물리 엔진에 객체지향(OOP)이 필요한가?

물리 시뮬레이션을 구현할 때 단순히 변수와 함수의 나열로 작성하면, 입자가 수천 개로 늘어나는 순간 코드는 관리 불능 상태가 됩니다. **객체지향 프로그래밍(OOP)**은 각 물리적 실체를 하나의 '객체'로 정의하여 데이터와 로직을 묶어줍니다.

특히 **캡슐화(Encapsulation)**를 통해 가속도, 속도, 위치와 같은 내부 상태를 보호하고, 정해진 메서드(`update`)를 통해서만 상태를 변화시키는 것이 중요합니다.

---

## 2. 물리 법칙의 코드화: 뉴턴의 제2법칙

시뮬레이션의 핵심은 뉴턴의 운동 법칙입니다.

$$\vec{F} = m\vec{a} \implies \vec{a} = \frac{\vec{F}}{m}$$

이 물리 공식은 코드 상에서 매 프레임마다 가속도를 계산하고, 이를 통해 속도와 위치를 갱신하는 방식으로 구현됩니다.

---

## 3. C++ 클래스 설계 (Source Code)

먼저 위치와 속도 계산을 편리하게 하기 위해 `Vector2D` 구조체를 정의하고, 이를 사용하는 `Particle` 클래스를 설계합니다.

```cpp
#include <iostream>
#include <vector>

// 2D 벡터 구조체: 연산자 오버로딩을 통한 직관적 계산
struct Vector2D {
    double x, y;

    Vector2D operator+(const Vector2D& v) const { return {x + v.x, y + v.y}; }
    Vector2D operator*(double scalar) const { return {x * scalar, y * scalar}; }
    void operator+=(const Vector2D& v) { x += v.x; y += v.y; }
};

// Particle 클래스: 캡슐화 적용
class Particle {
private:
    Vector2D position;
    Vector2D velocity;
    Vector2D acceleration;
    double mass;

public:
    Particle(Vector2D pos, double m) 
        : position(pos), velocity({0, 0}), acceleration({0, 0}), mass(m) {}

    // 힘을 가하는 메서드 (F = ma)
    void applyForce(Vector2D force) {
        Vector2D a = force * (1.0 / mass);
        acceleration += a;
    }

    // 상태 업데이트 (오일러 적분법)
    void update(double deltaTime) {
        velocity += acceleration * deltaTime;
        position += velocity * deltaTime;
        
        // 가속도 초기화 (매 프레임 힘의 합력을 새로 계산하기 위함)
        acceleration = {0, 0};
    }

    void display() const {
        std::cout << "Pos: (" << position.x << ", " << position.y << ")" << std::endl;
    }
};

int main() {
    // 질량 1.0인 입자를 (0,0)에 생성
    Particle p({0.0, 0.0}, 1.0);
    
    // 중력(가속도 개념의 힘) 적용 예시
    Vector2D gravity = {0.0, -9.8};
    
    std::cout << "--- Simulation Start ---" << std::endl;
    for (int i = 0; i < 5; ++i) {
        p.applyForce(gravity);
        p.update(0.1); // 0.1초 단위 업데이트
        p.display();
    }
    
    return 0;
}
```
```arduino
┌────────────────────────┐
│        Vector2D        │
├────────────────────────┤
│ + x : double           │
│ + y : double           │
├────────────────────────┤
│ + operator+(v) : Vector2D │
│ + operator*(scalar) : Vector2D │
│ + operator+=(v) : void │
└────────────────────────┘


┌────────────────────────┐
│        Particle        │
├────────────────────────┤
│ - position : Vector2D  │
│ - velocity : Vector2D  │
│ - acceleration : Vector2D │
│ - mass : double        │
├────────────────────────┤
│ + Particle(pos, m)     │
│ + applyForce(force) : void │
│ + update(deltaTime) : void │
│ + display() : void    │
└────────────────────────┘
            ▲
            │ (has-a)
            │
        Vector2D
```

## 4. 객체지향 설계의 핵심 포인트
캡슐화: position과 velocity를 private으로 두어 외부에서 직접 수정하는 것을 막았습니다. 오직 applyForce와 update를 통해서만 물리적 법칙에 따라 이동합니다.

단일 책임 원칙 (SRP): Particle 클래스는 자신의 물리 상태를 갱신하는 역할만 수행합니다. 렌더링이나 세계(World) 관리는 별도의 클래스에 맡기는 것이 좋습니다.

## 5. 마치며: 경제 모델로의 확장
이러한 **에이전트 기반 모델링(ABM)**은 경제학에서도 유용합니다. '입자'를 '가계'나 '기업'으로 바꾸고, '힘'을 '시장 이자율'이나 '소비 심리'로 치환하면 복잡한 경제 시스템을 시뮬레이션할 수 있는 기초가 됩니다.

다음 포스팅에서는 이 구조를 바탕으로 **상속(Inheritance)**을 이용해 다양한 물리적 성질을 가진 객체들을 만들어 보겠습니다.

## 💡 궁금한 점이 있으신가요?
C++ 설계 패턴이나 물리 시뮬레이션 구현 중 어려운 부분이 있다면 댓글로 남겨주세요!