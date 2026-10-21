Estes são os passos para utilizar o {{brand}} com o Gemini CLI e a aplicação Gemini.

> **Sobre a v{{version}}**
> Esta versão destina-se a experimentar a instalação no seu próprio ambiente. O funcionamento em cada ferramenta ainda não foi suficientemente verificado, pelo que alguns passos podem não funcionar como esperado.

## 1. Escolher o método de instalação

| Onde o quer utilizar | Método recomendado |
| --- | --- |
| Gemini CLI (as quatro em conjunto) | [A. Instalar como extensão](#a) |
| Gemini CLI (apenas as que precisar) | [B. Escolher e instalar skills](#b) |
| Aplicação Gemini (web, Mac, smartphone) | [C. Carregar as skills](#c) |

## A. Gemini CLI: instalar como extensão

Este método instala as quatro skills de uma só vez.

1. Transfira o [ZIP da extensão]({{plugin_url}}).
{{#if plugin_folder}}
2. Ao extrair o ZIP, é criada a pasta `{{plugin_folder}}`.
{{else}}
2. Crie uma pasta `{{plugin}}` vazia e extraia o ZIP para dentro dela.
{{/if}}
3. Instale indicando essa pasta.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Se aparecer um ecrã de confirmação, verifique o conteúdo antes de continuar. Depois de instalada, a extensão fica ativa em todos os projetos.

Se a instalou a partir de um ZIP, não é atualizada automaticamente. Quando sair uma nova versão, substitua-a pelo novo ZIP.

## B. Gemini CLI: escolher e instalar skills

Este método instala apenas as skills de que precisa, projeto a projeto. Se utilizou o método A, este passo não é necessário.

Por exemplo, para instalar `{{first}}`, execute o seguinte no projeto pretendido:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Para instalar outras skills, altere `--path` da seguinte forma:

{{gemini_paths}}

`--scope workspace` limita a utilização a «apenas este projeto». Se o omitir, a skill fica disponível em todos os seus projetos.

**Para atualizar**

Execute novamente o mesmo comando. A skill instalada é substituída; por isso, se a tiver alterado, guarde primeiro as suas alterações.

## C. Aplicação Gemini: carregar as skills

1. Transfira os ZIP das skills que quer utilizar.
{{skills_list_indented}}
2. No Gemini, abra **Customize** (ou **More**, se não o encontrar) → **Skills** → **Upload**.
3. Escolha os ZIP um a um, verifique as informações e prima **Create**.

**Atenção**

- Disponível apenas para contas Google pessoais de utilizadores com 18 anos ou mais. De momento, não funciona com contas de trabalho ou escolares.
- A opção «Keep Activity» (guardar atividade) tem de estar ativada.
- A funcionalidade está a ser disponibilizada gradualmente, pelo que pode ainda não lhe aparecer. Para mais informações, consulte a [ajuda oficial do Gemini](https://support.google.com/gemini/answer/17094296?hl=pt-PT).
- O ZIP da extensão (para o Gemini CLI) não funciona aqui.
- As skills carregadas não são atualizadas automaticamente. Quando sair uma nova versão, carregue-as novamente.

## 2. Experimentar

Para começar, recomendamos um pedido que não altere nenhum ficheiro.

> Vou preparar uma apresentação em português. A que aspetos devo prestar atenção? Não alteres nenhum ficheiro.

## Verificar os ficheiros (opcional)

Se quiser confirmar que os ficheiros transferidos não estão danificados, utilize o [SHA256SUMS.txt]({{sums}}).

Coloque o SHA256SUMS.txt na mesma pasta que os ficheiros ZIP transferidos e execute o seguinte comando num terminal. Se o `shasum` não estiver disponível, compare o SHA-256 com outra ferramenta, como o `Get-FileHash` do Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Se aparecer `OK` nas linhas dos ficheiros transferidos, está tudo em ordem.

---

Outras ferramentas: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Os ecrãs e as condições de disponibilidade podem mudar. Consulte as informações oficiais de cada serviço para obter os dados mais recentes (data de verificação desta página: 14 de outubro de 2026).
