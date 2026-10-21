Estes são os passos para utilizar o {{brand}} com o ChatGPT e o Codex.

> **Sobre a v{{version}}**
> Esta versão destina-se a experimentar a instalação no seu próprio ambiente. O funcionamento em cada ferramenta ainda não foi suficientemente verificado, pelo que alguns passos podem não funcionar como esperado.

## 1. Escolher o método de instalação

| Onde o quer utilizar | Método recomendado |
| --- | --- |
| ChatGPT (se for possível carregar skills) | [A. Adicionar as skills uma a uma](#a) |
| ChatGPT (para o registar como plugin pessoal) | [B. Registar tudo como plugin](#b) |
| Codex (no seu computador) | [C. Copiar as pastas](#c) |

Uma **skill** corresponde a uma função; o **plugin** é um pacote que reúne as quatro skills.

## 2. Transferir os ficheiros

Os ficheiros estão na [página da versão]({{release}}). Ao clicar numa ligação, o ficheiro ZIP é transferido.

**Plugin (as quatro skills reunidas)**

- {{plugin_link}}

**Skills (uma a uma)**

{{skills_list}}

## A. Adicionar skills ao ChatGPT

Este método pode ser utilizado se o ecrã do ChatGPT mostrar «Skills» com uma opção de carregamento.

1. Escolha um ficheiro ZIP de uma skill e carregue-o.
2. Verifique as informações apresentadas e adicione-a.
3. Repita os mesmos passos para cada skill de que precisar.

**Atenção**

- O ZIP do plugin não funciona com este método. Utilize os ZIP das skills.
- Anexar um ficheiro a uma conversa não o adiciona como skill.
- Se não encontrar a opção, é possível que ainda não esteja disponível no seu plano ou na sua aplicação. Consulte o [guia oficial da OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Registar um plugin no ChatGPT

Este método reúne as quatro skills e regista-as como o seu plugin pessoal.

1. Abra uma nova conversa no ChatGPT e selecione `@plugin-creator`.
2. Anexe o ficheiro ZIP do plugin.
3. Faça o pedido da seguinte forma:

   > Regista este pacote como o meu plugin privado. Não o submetas ao diretório público.

4. Depois de registado, **{{display}}** aparece em Plugins, em «Personal» ou «Created by me».
5. Instale-o, se necessário, e ative-o numa nova conversa.

**Atenção**

- O plugin pode ser registado no espaço de trabalho da sua equipa. Se quiser que seja só para si, verifique o destino antes de o registar.
- Consoante o seu plano ou as definições do espaço de trabalho, esta funcionalidade pode não estar disponível. Para mais informações, consulte [Build plugins](https://learn.chatgpt.com/docs/build-plugins) e [Plugins](https://learn.chatgpt.com/docs/plugins).
- Um plugin registado desta forma só pode ser utilizado pela sua conta. Não é publicado no diretório público.

## C. Copiar as pastas para o Codex

Ao extrair o ZIP de uma skill, obtém uma pasta como `{{first}}`. Copie essa pasta para o local que o Codex lê.

| Âmbito | Destino |
| --- | --- |
| Apenas num projeto específico | `.agents/skills/` dentro do projeto |
| Em todos os projetos | `~/.agents/skills/` na sua pasta pessoal |

Por exemplo, para adicionar `{{first}}` a um projeto:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Atenção**

- Copie a pasta inteira, com todo o conteúdo. Apenas com alguns ficheiros, a skill não funcionará corretamente.
- Se já existir uma pasta com o mesmo nome, verifique o conteúdo antes de a substituir.

## 3. Experimentar

Depois de instalar, abra uma nova conversa e chame a skill.

| Ferramenta | Como chamar |
| --- | --- |
| ChatGPT | Escolha a partir de `@` |
| Codex | Escolha a partir de `$` ou `/skills` |

Para começar, recomendamos um pedido que não altere nenhum ficheiro.

> Vou preparar um relatório em português. A que aspetos devo prestar atenção? Não alteres nenhum ficheiro.

## Verificar os ficheiros (opcional)

Se quiser confirmar que os ficheiros transferidos não estão danificados, utilize o [SHA256SUMS.txt]({{sums}}).

Coloque o SHA256SUMS.txt na mesma pasta que os ficheiros ZIP transferidos e execute o seguinte comando num terminal. Se o `shasum` não estiver disponível, compare o SHA-256 com outra ferramenta, como o `Get-FileHash` do Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Se aparecer `OK` nas linhas dos ficheiros transferidos, está tudo em ordem.

---

Outras ferramentas: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Os ecrãs e as condições de disponibilidade podem mudar. Consulte as informações oficiais de cada serviço para obter os dados mais recentes (data de verificação desta página: 14 de outubro de 2026).
