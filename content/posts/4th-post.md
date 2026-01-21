---
title: "C++ 팩토리 패턴(Factory Pattern): 객체 생성을 담당하는 스마트한 공장 세우기!!"
date: 2026-01-21
categories: [Programming, Design Patterns]
tags: [C++, OOP, FactoryPattern, DesignPatterns, Simulation]
math: true
comments: true
draft: false
summary: "수많은 물리 객체를 일일이 직접 만들고 계신가요? 이제 팩토리 패턴을 통해 객체 생성 로직을 깔끔하게 분리하고 관리를 자동화해 봅시다!!"
---

## 1. 자! 팩토리 패턴이 왜 필요한가요?

우리가 시뮬레이션을 만들다 보면 `GravityParticle`, `SmokeParticle` 등 수많은 객체가 필요해집니다!! 그런데 메인 코드 여기저기서 `new GravityParticle(...)`을 남발하면 어떻게 될까요? 

나중에 생성 로직이 바뀌면 모든 코드를 다 수정해야 하는 **'코드 지옥'**에 빠지게 됩니다!! 이때 **"객체 생성만 전문적으로 담당하는 공장"**을 하나 두면 모든 고민이 해결되지요!! 쉽죠?

---

## 2. 팩토리 패턴의 구조

팩토리 패턴은 부모 클래스 타입의 포인터를 반환하는 '공장 함수'를 만드는 것이 핵심입니다!!



---

## 3. C++ 팩토리 패턴 구현 코드!!

자! 코드를 직접 보면서 이해해 봅시다!! 어제 배운 `virtual`과 `override`가 어디에 쓰이는지 눈을 크게 뜨고 찾아보세요!!

```cpp
#include <iostream>
#include <string>
#include <memory>

// 1. 제품들의 부모 클래스 (추상적인 개념)
class Particle {
public:
    virtual ~Particle() {}
    virtual void showType() = 0; // 순수 가상 함수!!
};

// 2. 구체적인 제품들
class GravityParticle : public Particle {
public:
    void showType() override { std::cout << "중력 입자 생성 완료!!" << std::endl; }
};

class WindParticle : public Particle {
public:
    void showType() override { std::cout << "바람 입자 생성 완료!!" << std::endl; }
};

// 3. 마법의 공장 클래스!!
class ParticleFactory {
public:
    // 어떤 입자를 만들지 결정하는 공장 메서드
    static std::unique_ptr<Particle> createParticle(const std::string& type) {
        if (type == "gravity") {
            return std::make_unique<GravityParticle>();
        } else if (type == "wind") {
            return std::make_unique<WindParticle>();
        }
        return nullptr;
    }
};

int main() {
    // 공장에게 주문만 하면 끝!! 직접 new를 쓸 필요가 없어요!!
    auto p1 = ParticleFactory::createParticle("gravity");
    auto p2 = ParticleFactory::createParticle("wind");

    if (p1) p1->showType();
    if (p2) p2->showType();

    return 0;
}
```
## 4. 팩토리 패턴의 엄청난 장점!!
결합도 감소!!: 메인 코드는 구체적인 자식 클래스 이름을 몰라도 됩니다!! 그냥 공장에 "이거 줘!"라고 말만 하면 되니까요!!

유지보수 짱!!: 새로운 입자(예: MagicParticle)가 추가되어도, 공장 코드만 살짝 수정하면 끝납니다!! 다른 곳은 건드릴 필요가 없죠!!

조건부 생성: 물리 환경 설정에 따라 "A 상황엔 1번 객체, B 상황엔 2번 객체"를 공장 안에서 똑똑하게 판단해서 만들어줄 수 있습니다!!

## 5. 경제 시뮬레이션에서의 응용!!
경제 시뮬레이션에서도 이 패턴은 빛을 발합니다!!

AgentFactory를 만들어서, 시장 상황에 따라 '공격적인 투자자'나 '보수적인 저축가'를 자동으로 생성하여 시장에 투입할 수 있지요!! 정말 멋지지 않나요?

## 💡 공장장이 되어보신 소감이 어떠신가요?
팩토리 패턴을 적용하면 여러분의 코드가 한결 전문적으로 변한답니다!! 이해가 안 가는 부분이 있다면 언제든 질문해 주세요!! 다음 시간에는 이 객체들을 한 번에 관리하는 **싱글톤 패턴(Singleton)**에 대해 알아볼까요?