Estes são os passos para utilizar o {{brand}} com o Claude Code e o chat do Claude.

> **Sobre a v{{version}}**
> Esta versão destina-se a experimentar a instalação no seu próprio ambiente. O funcionamento em cada ferramenta ainda não foi suficientemente verificado, pelo que alguns passos podem não funcionar como esperado.

## 1. Escolher o método de instalação

| Onde o quer utilizar | Método recomendado |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Instalar a partir do GitHub](#a) (atualização fácil) |
{{/if}}
| Claude Code (para instalar a partir de um ZIP) | [{{L_zip}}. Instalar a partir de um ZIP](#{{l_zip}}) |
| Chat do Claude (claude.ai e aplicações) | [{{L_chat}}. Carregar as skills](#{{l_chat}}) |

O Claude Code e o chat do Claude instalam-se de formas diferentes.

{{#if marketplace}}
## A. Claude Code: instalar a partir do GitHub

1. Num terminal, registe a origem de distribuição do KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Numa conversa do Claude Code, introduza o seguinte:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Verifique as informações, escolha o âmbito (só para si, só para este projeto, etc.) e instale.

Depois de instalado, passa a poder utilizar os seguintes comandos.

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: instalar a partir de um ZIP

1. Transfira o [ZIP do plugin para o Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Ao extrair o ZIP, é criada a pasta `{{plugin_folder}}`.
{{else}}
2. Crie uma pasta `{{plugin}}` vazia e extraia o ZIP para dentro dela.
{{/if}}
3. Inicie o Claude Code indicando essa pasta.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Atenção**

- Utilize o conteúdo da pasta tal como está. Não remova ficheiros nem acrescente outros.
- Este método não é atualizado automaticamente. Quando sair uma nova versão, substitua-a pelo novo ZIP.

## {{L_chat}}. Chat do Claude: carregar as skills

Este método aplica-se ao claude.ai e às aplicações do Claude.

1. Transfira os ZIP das skills que quer utilizar.
{{skills_list_indented}}
2. No Claude, abra **Customize → Skills** e escolha **Upload a skill** no botão de adicionar.
3. Carregue os ZIP um a um e ative cada skill.

**Atenção**

- O ZIP do plugin para o Claude Code não funciona aqui. Utilize os ZIP das skills.
- Carregue os ZIP sem alterar o nome dos ficheiros.
- Para utilizar skills, a execução de código tem de estar ativada nas definições. Para mais informações, consulte o [guia oficial do Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Em contas de organização, pode não estar disponível consoante as definições do administrador.
- As skills carregadas não são atualizadas automaticamente. Quando sair uma nova versão, carregue-as novamente.

## 2. Experimentar

Para começar, recomendamos um pedido que não altere nenhum ficheiro.

> Vou criar uma página web em português. A que aspetos devo prestar atenção? Não alteres nenhum ficheiro.

## Verificar os ficheiros (opcional)

Se quiser confirmar que os ficheiros transferidos não estão danificados, utilize o [SHA256SUMS.txt]({{sums}}).

Coloque o SHA256SUMS.txt na mesma pasta que os ficheiros ZIP transferidos e execute o seguinte comando num terminal. Se o `shasum` não estiver disponível, compare o SHA-256 com outra ferramenta, como o `Get-FileHash` do Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Se aparecer `OK` nas linhas dos ficheiros transferidos, está tudo em ordem.

---

Outras ferramentas: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Os ecrãs e as condições de disponibilidade podem mudar. Consulte as informações oficiais de cada serviço para obter os dados mais recentes (data de verificação desta página: 14 de outubro de 2026).
