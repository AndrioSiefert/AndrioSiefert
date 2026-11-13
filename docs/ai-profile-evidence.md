# Evidências para o destaque de IA no perfil

Análise somente de leitura dos projetos fornecidos pelo usuário em 13/11/2026. A mudança é no perfil; nenhum runtime, configuração, credencial ou dado de negócio foi alterado. Não foram executadas inferências nem as suítes dos projetos de origem.

| Destaque publicado | Evidência consultada | Limite da afirmação |
| --- | --- | --- |
| OpenAI e OpenRouter | Confirmação do usuário; currículo (OpenAI Responses API); `naMoska_AI/src/namoska_ai/adapters/outbound/providers/openrouter_structured_generation.py` e `openrouter_vision_structured_generation.py` | O código atual usa OpenRouter com cliente compatível OpenAI. A experiência direta com OpenAI é sustentada pelo usuário e currículo, não inferida do nome do SDK. |
| Extração multimodal de imagens e PDFs | `naMoska_AI/src/namoska_ai/capabilities/purchase_document_image_extract.py`, `adapters/outbound/images/pillow_document_images.py`, `docs/purchase-document-evaluation.md` | Extração gera rascunhos com revisão humana. Não se afirma precisão comprovada nem homologação dos documentos reais. |
| Saídas estruturadas e contratos tipados | Adaptadores OpenRouter de texto/visão; modelos Pydantic da capacidade de extração | JSON Schema e validação de contrato não garantem fidelidade semântica dos valores extraídos. |
| Agentes com ferramentas MCP e revisão humana | `naMoska_Agent/src/relay/data-plane.ts`, `src/catalog/tool-allowlist.ts`, `docs/architecture.md` | Integração do runtime Hermes existente. Ferramentas de leitura e preparação; confirmação de mudanças permanece na aplicação. |
| Isolamento por execução | `naMoska_Agent/src/lanes/lane.ts` | Lease, delegação e quarentena no relay. Não se afirma certificação ou segurança absoluta. |
| Orçamento de tokens e observabilidade | `naMoska_Agent/test/hermes/test_namoska_budget.py`; `naMoska_AI/src/namoska_ai/application/execution_usage.py`; seção de contabilização em `docs/purchase-document-evaluation.md` | Recursos implementados e cobertos por testes documentados. Não foi medida economia de custo nesta tarefa. |
| Avaliação e testes sintéticos | `naMoska_AI/docs/purchase-document-evaluation.md`, `tests/unit/test_purchase_document_dense_photo.py` e testes de saída estruturada | Validação offline/sintética não é resultado de produção. Nenhum benchmark numérico foi adicionado ao perfil. |

O README usa descrições de capacidade, sem expor documentos privados, segredos, endpoints internos ou transcrições. Os nomes dos dois projetos foram fornecidos para esta análise; não foram criados links públicos presumindo repositórios acessíveis.
