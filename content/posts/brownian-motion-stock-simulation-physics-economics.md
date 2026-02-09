---
title: "물리학자가 주가를 예측하는 법: 브라운 운동과 몬테카를로 시뮬레이션 (C++ & Python)"
date: 2026-02-09
draft: false
description: "아인슈타인의 브라운 운동이 금융 공학의 핵심이라는 사실을 아시나요? 기하 브라운 운동(GBM) 모델을 C++로 고속 시뮬레이션하고 Python으로 분석하여 주가 흐름을 공학적으로 예측해봅니다."
categories: ["Physics", "Economics", "Programming"]
tags: ["Brownian Motion", "Monte Carlo", "Quant", "C++", "Python", "Simulation", "Financial Engineering"]
author: "ShyEngineer"
cover:
  image: "images/brownian-motion-stock-simulation-cover.png" # 주인님, 이 이미지는 WEBP로 변환 부탁드립니다!
  alt: "Monte Carlo Simulation Paths"
  caption: "무작위 행보(Random Walk)로 생성된 수만 개의 주가 시나리오"
---

## 1. 꽃가루의 춤과 월스트리트의 차트

1827년, 식물학자 로버트 브라운은 물에 띄운 꽃가루 입자가 불규칙하게 움직이는 현상을 발견했습니다. 그리고 1905년, **알베르트 아인슈타인**은 이 불규칙한 움직임이 물 분자와의 충돌 때문임을 수학적으로 증명했죠. 이것이 바로 **브라운 운동(Brownian Motion)**입니다.

그런데 놀랍게도, 이 물리학 공식이 **주식 시장의 가격 변동**을 설명하는 데 그대로 사용됩니다.

> **💡 Insight:**
> 액체 속의 입자가 수조 개의 물 분자와 충돌하며 무작위로 움직이듯, 주가는 수많은 매수/매도 주문과 충돌하며 무작위 행보(Random Walk)를 합니다.

이번 글에서는 금융 공학의 기초가 되는 **기하 브라운 운동(GBM)** 모델을 이해하고, **C++의 강력한 성능**으로 수십만 번의 시뮬레이션을 돌린 뒤, **Python**으로 그 결과를 분석해보겠습니다.

---

## 2. 물리학 수식에서 금융 모델로 (Theory)

입자의 확산을 다루는 확률 미분 방정식(SDE)을 주가($S_t$)에 적용하면 다음과 같은 식이 나옵니다.

$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

이 수식은 두 부분으로 나뉩니다:
1.  **Drift ($\mu S_t dt$)**: 주가의 장기적인 **기대 수익률** (방향성).
2.  **Diffusion ($\sigma S_t dW_t$)**: 시장의 **변동성** (무작위 충격, 위너 과정).

우리는 이 미분 방정식을 컴퓨터가 이해할 수 있는 이산 시간 모델(Discrete Time Model)로 바꿔야 합니다. 이를 **오일러-마루야마(Euler-Maruyama) 근사**라고 합니다.

$$S_{t+\Delta t} = S_t \exp \left( (\mu - \frac{1}{2}\sigma^2)\Delta t + \sigma \sqrt{\Delta t} Z \right)$$

여기서 $Z$는 표준 정규 분포 $N(0, 1)$을 따르는 난수입니다.

---

## 3. Engineering: C++ 고속 시뮬레이션 엔진

Python은 데이터 분석에 좋지만, 수백만 번의 반복 연산이 필요한 **몬테카를로 시뮬레이션(Monte Carlo Simulation)**에서는 C++가 압도적인 성능을 발휘합니다.

주인님께서 익숙하신 모던 C++ 스타일(`std::vector`, `<random>`)로 엔진을 구현했습니다.

```cpp
// simulation_engine.cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <fstream>
#include <string>

// 시뮬레이션 파라미터 구조체
struct SimulationParams {
    double S0;      // 초기 주가
    double mu;      // 연간 기대 수익률 (Drift)
    double sigma;   // 연간 변동성 (Volatility)
    double T;       // 기간 (년)
    int steps;      // 시간 간격 수
    int simulations; // 시뮬레이션 횟수
};

void run_simulation(const SimulationParams& params, const std::string& filename) {
    std::ofstream file(filename);
    file << "Time,Path_ID,Price\n";

    double dt = params.T / params.steps;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<> d(0, 1); // 표준 정규 분포 Z ~ N(0, 1)

    // 성능 최적화를 위해 미리 계산
    double drift = (params.mu - 0.5 * params.sigma * params.sigma) * dt;
    double diffusion = params.sigma * std::sqrt(dt);

    for (int i = 0; i < params.simulations; ++i) {
        double current_price = params.S0;
        file << 0 << "," << i << "," << current_price << "\n";

        for (int t = 1; t <= params.steps; ++t) {
            double Z = d(gen); // 무작위 충격 생성
            
            // GBM 공식 적용
            current_price = current_price * std::exp(drift + diffusion * Z);
            
            file << t * dt << "," << i << "," << current_price << "\n";
        }
    }
    
    std::cout << "Simulation Complete: " << params.simulations << " paths generated." << std::endl;
    file.close();
}

int main() {
    // 예: 초기가 100불, 기대수익률 5%, 변동성 20%, 1년, 252일(거래일), 1000번 시뮬레이션
    SimulationParams params = {100.0, 0.05, 0.2, 1.0, 252, 1000};
    run_simulation(params, "stock_paths.csv");
    return 0;
}
```
> **🛠️ Code Review:**
> * **`std::mt19937`**: 메르센 트위스터 알고리즘을 사용하여 고품질의 난수를 생성합니다. 금융 시뮬레이션에서 난수의 품질은 매우 중요합니다.
> * **`exp` 연산 최적화**: 루프 밖에서 상수를 미리 계산하여 연산 비용을 줄였습니다.


## 4. Analysis: Python으로 미래 시각화하기

C++이 생성한 `stock_paths.csv` 데이터를 Python으로 불러와 시각화해 봅시다. 여기서 우리는 주가의 **불확실성(Risk)**을 눈으로 확인할 수 있습니다.

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 데이터 로드
df = pd.read_csv('stock_paths.csv')

# 시각화 설정
plt.figure(figsize=(12, 6))
plt.title('Monte Carlo Simulation: Geometric Brownian Motion', fontsize=16, fontweight='bold')
plt.xlabel('Time (Year)')
plt.ylabel('Stock Price ($)')

# 각 시뮬레이션 경로 그리기 (Pivot 활용)
pivot_df = df.pivot(index='Time', columns='Path_ID', values='Price')
plt.plot(pivot_df, alpha=0.1, color='blue', linewidth=1)

# 평균 경로 (붉은색 점선)
plt.plot(pivot_df.mean(axis=1), color='red', linewidth=3, linestyle='--', label='Expected Mean')

# 신뢰 구간 (95%)
final_prices = pivot_df.iloc[-1]
quantile_05 = np.percentile(final_prices, 5)
quantile_95 = np.percentile(final_prices, 95)

plt.axhline(y=quantile_05, color='green', linestyle=':', label='95% Confidence Low')
plt.axhline(y=quantile_95, color='green', linestyle=':', label='95% Confidence High')

plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()

print(f"95% 확률로 주가는 ${quantile_05:.2f} 에서 ${quantile_95:.2f} 사이에 존재합니다.")
```

### 📊 분석 결과 (Interpretation)
* **확산(Diffusion):** 시간이 지날수록 그래프의 폭(변동성)이 넓어집니다. 이는 미래가 멀어질수록 예측의 불확실성이 커짐을 의미합니다. (엔트로피 증가와 유사하죠!)
* **평균 회귀?** 개별 경로는 미친 듯이 날뛰지만, 수만 번의 평균(빨간 점선)은 우리가 설정한 기대 수익률($\mu$)을 따라갑니다.
* **Risk Management:** 우리는 주가가 정확히 얼마가 될지는 모르지만, **"최악의 경우 어디까지 떨어질 수 있는지(VaR)"**는 확률적으로 계산할 수 있습니다. 이것이 공학적 투자의 핵심입니다.

---

## 5. 마치며: 코드로 읽는 세상

우리는 오늘 **물리학의 입자 운동 방정식**을 이용해 **금융 시장의 불확실성**을 시뮬레이션했습니다.

* **C++**은 복잡한 자연 현상을 빠르게 계산하는 **엔진(Engine)** 역할을,
* **Python**은 그 결과를 해석하여 통찰을 주는 **대시보드(Dashboard)** 역할을 수행했습니다.

경제학은 '보이지 않는 손'을 말하지만, 공학자는 그 손의 움직임을 **데이터와 코드**로 시각화합니다. 이것이 제가 엔지니어링을 사랑하는 이유입니다.

다음 포스팅에서는 이 모델에 **"점프 확산(Jump Diffusion - 갑작스런 폭락)"**을 추가하여 더 현실적인 모델을 만들어보겠습니다. 기대해 주세요!

---
**[참고 문헌 및 도구]**
* **C++ Reference:** `<random>`, `<fstream>`
* **Python Libs:** `pandas`, `matplotlib`
* **Theory:** Hull, J. C. "Options, Futures, and Other Derivatives"