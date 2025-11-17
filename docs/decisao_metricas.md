# Métrica utilizada pelo scikit-multiflow (agente)

-- A biblioteca **scikit-multiflow** fornece vários detectores (ADWIN, PageHinkley, DDM, EDDM, KSWIN, HDDM_A, HDDM_W). Neste repositório, DDM e EDDM foram removidos do fluxo de trabalho por não serem adequados para detecção de mudanças em valores contínuos.
- As métricas foram estabelecidas pelo agente que implementou o teste da biblioteca

Sendo:
### True Positive (TP)

Uma detecção é considerada **True Positive** quando satisfaz **todos** os seguintes critérios:

1. **Existe um evento ground-truth** no dataset (marcador `regime_change == 1`)
2. A detecção ocorre **dentro de uma janela de tolerância** após o evento real
3. **Condição matemática**: `0 <= (sample_detecção - sample_ground_truth) <= tolerance`
4. O evento ground-truth **não foi previamente matched** por outra detecção
5. Se múltiplas detecções qualificam, escolhe-se a com **menor delay** (mais próxima)

Portanto:
- As detecções feitas antes do GT não são consideradas TP.
- Se houver alguma TP dentro da janela, apenas a primeira detecção será a TP.

Pergunta a esclarecer:
- E se houverem muitas detecções dentro da janela, isso afeta o score?
	- Reposta: é detectado como FP.
- Qual o tamanho da janela selecionado?

### False Positive (FP)

Uma detecção é considerada **False Positive** quando:

- **NÃO existe nenhum evento ground-truth** dentro da janela de tolerância após a detecção
- **OU** o evento ground-truth mais próximo **já foi matched** por outra detecção anterior
#### Cenários Típicos de FP

1. **Ruído do sinal**: Detector reage a artefatos ou variações normais
2. **Transições entre registos**: Mudança de baseline ao concatenar múltiplos pacientes
3. **Parâmetros muito sensíveis**: `delta` muito baixo gera detecções espúrias
4. **Detecção tardia**: Delay > tolerance (passou do prazo)
5. **Detecção antecipada**: Antes do evento começar (impossível em streaming real)

### False Negative (FN)

Um evento ground-truth é considerado **False Negative** quando:

- **Nenhuma detecção** foi associada (matched) a esse evento
- Ou seja, eventos reais que o detector **falhou em identificar**
#### Cenários Típicos de FN

1. **Parâmetros pouco sensíveis**: `delta` muito alto não reage a mudanças sutis
2. **Janela de média móvel grande**: Suavização excessiva mascara o evento
3. **Min-gap muito alto**: Suprime detecções próximas a eventos anteriores
4. **Mudanças graduais**: Transições lentas que não ultrapassam o threshold
5. **Eventos de curta duração**: Regimes muito breves não geram sinal suficiente

# Métrica utilizada no Classification Score Stream (ClaSS)
link: https://github.com/ermshaua/classification-score-stream
DOI: [10.14778/3659437.3659450](https://dl.acm.org/doi/10.14778/3659437.3659450)

## Covering

A métrica "Covering", da forma como é descrita no artigo, permite que uma deteção seja considerada válida (ou seja, contribua positivamente para a pontuação) mesmo que o segmento previsto não se alinhe perfeitamente com o "ground truth", desde que exista **sobreposição** entre eles.

A métrica funciona da seguinte forma:

1. **Foco nos Segmentos:** A métrica não avalia primariamente os "pontos de mudança" (Change Points), mas sim os "segmentos" (os intervalos _entre_ os pontos de mudança).
2. **Medição de Sobreposição (Overlap):** Ela "quantifica o grau exato de sobreposição entre os segmentos previstos e os segmentos anotados ('ground truth')".
3. **Uso do Índice Jaccard:** Para encontrar a melhor correspondência, a métrica utiliza o índice Jaccard, que mede a interseção dividida pela união de dois conjuntos (neste caso, os dois segmentos temporais).

Portanto, se um segmento previsto começar _antes_ do segmento "ground truth", mas tiver uma sobreposição temporal com ele, essa sobreposição resultará numa pontuação Jaccard positiva, contribuindo para a pontuação final do "Covering".

## Detecção de eventos em streaming com janela de latência aceitável e deduplicação

O problema não é de *segmentação* pura, mas sim de *deteção de eventos* com restrições temporais. A solução é usar um algoritmo de "correspondência de eventos" (event matching) para contar os TPs, FPs e FNs, e *depois* calcular o F1-Score.

### Racional

1.  **Ground Truth (GT):** Os pontos de mudança verdadeiros.
2.  **Janela de Aceitação:** A deteção deve ocorrer *após* o evento GT, num intervalo de 0 a 10 segundos.
3.  **Janela de Objetivo:** A deteção *ideal* ocorre entre 0 e 4 segundos.
4.  **Falha (Miss):** Se não houver uma deteção dentro dos 10 segundos é um FN.
5.  **Deteção Múltipla:** Várias deteções para o mesmo evento GT (dentro da janela de 10s) contam como *uma* só deteção correta, não como FPs adicionais.
6.  **Deteção Antecipada:** Uma deteção *antes* de um evento GT é irrealista no streaming e deve ser tratada como um Falso Positivo.

### Métricas

1. **F1-Score com Janela Temporal Adaptativa** (Métrica Principal)

**Hit@τ (Recall@τ):** $$\text{Recall@}\tau=\frac{\text{TP}}{\text{TP}+\text{FN}}$$
→ “Que fração das mudanças foi apanhada em até $\tau$ s?”

**Precision@τ:**  $$\text{Precision@}\tau=\frac{\text{TP}}{\text{TP}+\text{FP}}$$
→ “Das coisas que alertei, quantas eram mudanças reais?”

**Vantagens:**
- Independente do tamanho da série
- Não penaliza múltiplas detecções dentro da janela aceitável
- Funciona com número variável de mudanças

2. **Time-Aware Covering Score**, uma métrica que considera a qualidade temporal das detecções

3. **Annotation/No-Annotation Score (NAB-inspired)** Numenta Anomaly Benchmark
- valoriza os alertas rápidos, mas não penaliza excessivamente os mais lentos (dentro do limite).
- Ignora detecções repetidas dentro da janela aceitável.
- Penaliza separadamente os FP.
- **O Range de scores pode ser entre um valor muito negativo (se houver muitos FPs) até +X, (sendo X o número total de anomalias).**

**Diferenças filosóficas entre NAB e F3-score ponderado**
- NAB (Aditivo):
    O score final é uma soma de recompensas e custos fixos.
    Score = (Soma TPs Ponderados) - (Contagem FPs * 0.11) - (Contagem FNs * 1.0)
    Neste modelo, um Falso Positivo custa-lhe sempre -0.11 pontos. Este custo é fixo e absoluto. Não importa se você acertou 100 TPs ou 2 TPs, o FP custa-lhe sempre o mesmo. Isto simula um custo operacional **(ex: "cada alarme falso custa 5 minutos de um engenheiro").**

- Seu F3-Ponderado (Rácio):
    O score final é um rácio (uma média harmónica de rácios)
    F3 = MédiaHarmónica(Precision_Ponderada, Recall_Ponderado)
    O "custo" de um Falso Positivo é relativo. O FP entra na componente de Precision ($TP_w / (TP_w + FP)$).

    - Se $TP_w$ for muito alto (muitos TPs bem detetados), um FP extra tem um impacto _pequeno_ na Precision.

    - Se $TP_w$ for baixo (poucos TPs), um FP extra tem um impacto _enorme_ na Precision.


2. Métricas de robustez/produção
- **MTFA (Mean Time Between False Alarms)** e/ou **FP/min** → sinalizam “ruído do modelo”.
- **Recall@4s vs. Recall@10s** → mostrares dois números dá transparência clínica: “apanhei X% até 4s e Y% até 10s”.


Combinação:
1. **Métrica Principal**: F1-Score com janela temporal (para comparabilidade com literatura)
2. **Métrica Secundária**: Time-Aware Covering Score (para avaliar qualidade temporal)
3. **Métricas Auxiliares**:
   - Detection Rate (recall puro)
   - False Alarm Rate normalizada por tempo
   - Delay médio das detecções corretas

Esta abordagem permite:
- Comparar séries de tamanhos diferentes
- Não considerar detecções antecipadas (janela unidirecional)
- Funcionar com número variável de mudanças (sem necessidade de pré-definir K)
- Valorizar detecções rápidas sem penalizar excessivamente as mais lentas (dentro do limite)


---

Considerando a análise feita acima, vamos precisar de mais de uma métrica para avaliar os detectores de regime:

- F-Score, para comparabilidade com literatura
- F-Score ponderado por latência.
- Recall@$\tau$ sendo $\tau$ o limite ótimo de latência (4s) e 10s
- Precision@$\tau$ sendo $\tau$ o limite ótimo de latência (4s) e 10s
- MTFA (Mean Time Between False Alarms) ou FP/min
- EDD (Expected Detection Delay)
- NAB Score, para avaliar a robustez operacional
