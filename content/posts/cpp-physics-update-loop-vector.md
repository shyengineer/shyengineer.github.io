---
title: "C++ 물리 엔진의 심장: 효율적인 업데이트 루프와 벡터(std::vector) 관리 기술!!"
date: 2026-01-25
categories: [Programming, Physics]
tags: [C++, OOP, Simulation, UpdateLoop, Optimization]
math: true
comments: true
draft: false
summary: "싱글톤 관리자가 수많은 객체를 한 번에 처리하는 메커니즘을 배웁니다! 데이터의 연속성을 활용한 성능 최적화와 안정적인 루프 설계법을 공개합니다!!"
---

## 1. 업데이트 루프(Update Loop): 시뮬레이션의 심장박동!!

물리 시뮬레이션은 멈춰있는 사진이 아니라 흐르는 영화와 같습니다!! 관리자는 매 찰나(Frame)마다 모든 객체에게 "자, 다음 위치로 이동해!"라고 명령을 내려야 하죠. 이 반복되는 과정을 **업데이트 루프**라고 부릅니다!!

보통 아래와 같은 순서로 진행돼요:
1. **입력 처리:** 사용자나 시스템의 명령을 듣습니다.
2. **물리 업데이트:** 모든 객체의 가속도, 속도, 위치를 계산합니다.
3. **렌더링:** 계산된 결과를 화면에 그립니다.

---

## 2. 수많은 객체를 담는 그릇: std::vector!!

관리자가 객체들을 효율적으로 돌보려면 한 곳에 잘 모아두어야 합니다. C++에서 가장 사랑받는 그릇은 바로 `std::vector`입니다!!



왜 `std::vector`일까요? 
* **메모리 밀집도:** 데이터가 메모리상에 나란히 붙어 있어, CPU가 다음 객체를 찾을 때 속도가 빛처럼 빠릅니다!!
* **유연함:** 새로운 입자가 태어나거나(Factory 이용), 수명이 다해 사라질 때 관리가 매우 용이합니다!!

---

## 3. 효율적인 관리자 코드 구현!!

지난번에 만든 싱글톤 `PhysicsWorld`에 객체 관리 기능을 추가해 봅시다!!

```cpp
#include <iostream>
#include <vector>
#include <memory>

class PhysicsWorld {
private:
    // 관리할 입자들을 담는 벡터 (다형성 활용!!)
    std::vector<std::unique_ptr<Particle>> particles;

    PhysicsWorld() {}
    PhysicsWorld(const PhysicsWorld&) = delete;
    PhysicsWorld& operator=(const PhysicsWorld&) = delete;

public:
    static PhysicsWorld& getInstance() {
        static PhysicsWorld instance;
        return instance;
    }

    // 입자 추가 (팩토리에서 만든 객체를 전달받음!!)
    void addParticle(std::unique_ptr<Particle> p) {
        particles.push_back(std::move(p));
    }

    // 핵심 업데이트 루프!!
    void update(double deltaTime) {
        // 모든 입자를 순회하며 물리 법칙 적용!!
        for (auto& p : particles) {
            p->update(deltaTime); 
        }
        std::cout << particles.size() << "개의 입자가 움직이고 있습니다!!\n";
    }
};
```
## 4. 최적화 꿀팁: 데이터 관리의 핵심!!
객체가 많아질수록 성능이 중요해집니다!! 관리자로서 다음 두 가지를 꼭 기억하세요!!

불필요한 객체 삭제: 화면 밖으로 나가거나 수명이 다한 입자는 바로바로 벡터에서 제거해야 합니다. 그렇지 않으면 '유령 객체'들이 CPU를 계속 괴롭힐 거예요!!

Reserve 활용: 벡터의 크기가 커질 때 메모리를 새로 할당하는 비용은 꽤 큽니다. 대략적인 개수를 안다면 particles.reserve(1000);으로 미리 공간을 확보하세요!!

## 5. 경제 모델로의 응용: 시장의 순환!!
이 루프는 경제 시뮬레이션에서 **'회계 연도'**나 **'거래 주기'**가 됩니다!! 싱글톤인 Market 관리자가 모든 Agent(가계, 기업)를 순회하며 수입과 지출을 계산하고, 파산한 주체는 리스트에서 제거하며 시스템을 유지하는 것과 똑같은 원리랍니다!!

💡 관리자의 업무를 자동화한 소감이 어떠신가요?
이제 여러분의 물리 세계는 스스로 숨 쉬며 움직일 준비가 끝났습니다!! 수천 개의 입자가 동시에 춤추는 모습, 상상만 해도 짜릿하지 않나요?

혹시 "수만 개가 넘어가니 너무 느려져요!" 하시는 분 계신가요? 다음 시간에는 성능을 극한으로 끌어올리는 공간 분할(Spatial Partitioning) 기법에 대해 알아볼까요?

언제든 여러분의 생각을 댓글로 들려주세요!! 함께 멋진 엔진을 완성해 봅시다!!