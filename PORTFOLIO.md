# Redp4w / manutenção do perfil

A página principal é `README.md`; `assets/hero.svg` é o banner.

Para atualizar **skills** ou **certificados**, use os comentários `SKILLS` e
`CERTIFICADOS` dentro do README. Copie o bloco de imagem ou link correspondente,
substitua o endereço e acrescente `alt` e `title` para acessibilidade.
Não altere a seção entre `<!-- LATEST:START -->` e `<!-- LATEST:END -->`:
essa região é sincronizada pela Action já existente.

O site concentra as notas em `redp4w.github.io/_posts/`. Ao publicar uma nota nova,
o Jekyll atualiza `/arquivo/` e `/latest.json`; a Action do perfil consulta esse JSON
periodicamente. Nenhum script precisa ser executado no computador pessoal.

Mantenha os SVGs existentes em `assets/`. O painel TryHackMe permanece um snapshot
datado até ser atualizado; não deve ser apresentado como status ao vivo.
