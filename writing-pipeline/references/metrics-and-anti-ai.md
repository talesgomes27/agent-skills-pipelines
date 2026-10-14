# Métricas Operacionais e Anti-IA

## 1. Cinco Métricas Verificáveis

### 1.1 Burstiness e Comprimento por Arquétipo

- **Arquétipo A (Data Science / Quarto) e Prosa Argumentativa (PRDs / ADRs)**:
  - Mínimo por frase: 3 a 6 palavras (impacto).
  - Máximo por frase: 22 a 32 palavras (articulação).
  - Desvio padrão mínimo: 6,5 palavras por parágrafo.
  - Pelo menos 15% das frases por parágrafo devem ter < 8 palavras.
- **Arquétipo B (Software / APIs / Docstrings)**:
  - Foco em precisão contratual: frases médias de 10 a 18 palavras (sem exigência de frases longas de 22–32 palavras ou DP ≥ 6,5).
- **Arquétipo C (CLI / Scripts / POSIX)**:
  - Foco telegráfico e imperativo: frases curtas de 5 a 12 palavras, zero prosa (dispensado de DP ≥ 6,5).

### 1.2 Índice de Tells de IA

Zero ocorrências das palavras:
- Adjetivos: robusto, vital, crucial, inovador, revolucionário,
  escalável, seamless, poderoso, abrangente.
- Substantivos: orquestração perfeita, sinergia, ecossistema.
- Fórmulas: "não apenas X, mas Y", "não se trata de X, mas de Y".

### 1.3 Falsos Contrastes

Padrão proibido: "não apenas... mas também", "não se trata de...
mas de". Zero ocorrências.

### 1.4 Gerundismos Decorativos

Proibido usar gerúndio de consequência decorativa:
- "garantindo assim..."
- "evidenciando a necessidade de..."
- "possibilitando que..."
- "permitindo que..."

### 1.5 Frases Curtas

Pelo menos 15% das frases de cada parágrafo devem ter < 8 palavras.

## 2. Blacklist de Palavras e Expressões

### 2.1 Adjetivos Vazios (PT-BR)
robusto, vital, crucial, inovador, revolucionário, escalável,
poderoso, abrangente, holístico, sinérgico, diferenciado,
disruptivo, de ponta, estado-da-arte.

### 2.2 Adjetivos Vazios (EN)
robust, vital, crucial, innovative, revolutionary, scalable,
seamless, powerful, comprehensive, holistic, synergistic,
cutting-edge, state-of-the-art, game-changing.

### 2.3 Fórmulas
- "não apenas X, mas Y"
- "não se trata de X, mas de Y"
- "not only X, but also Y"
- "it's not about X, it's about Y"

### 2.4 Travessões Duplos
Proibido usar `—` para conectar orações independentes. Usar ponto,
ponto-e-vírgula ou reescrever.

## 3. Checklist de 10 Itens para Revisão

1. [ ] Parágrafo abre com dado concreto, sem preâmbulos.
2. [ ] Alternância entre frases curtas e longas.
3. [ ] Zero adjetivos de marketing.
4. [ ] Zero falsos contrastes.
5. [ ] Zero travessões duplos conectando orações independentes.
6. [ ] Listas assimétricas (sem negrito obrigatório).
7. [ ] Pessoa gramatical consistente com o arquétipo.
8. [ ] Citações rastreáveis (manifesto ou link inline).
9. [ ] Conclusão encerra no último resultado útil.
10. [ ] Texto soa como relato de engenheiro sênior.
