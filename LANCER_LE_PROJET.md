# Où ouvrir et comment lancer le projet

Ce projet se lance depuis un terminal dans le dossier du dépôt Git. Il n'y a pas encore d'interface web à ouvrir dans un navigateur : la version actuelle est une fondation technique avec des schémas, des exemples JSON, des tests et un script de vérification local.

## 1. Ouvrir le dossier

Dans VS Code ou Cursor :

1. Clique sur **File** → **Open Folder**.
2. Sélectionne le dossier du repo :

```text
/workspace/TaskMaksimTest
```

3. Ouvre le terminal intégré :
   - VS Code / Cursor : **Terminal** → **New Terminal**.

Si tu es déjà dans un terminal, va directement dans le dossier :

```bash
cd /workspace/TaskMaksimTest
```

## 2. Lancer le test principal

Dans le terminal ouvert à la racine du projet, lance :

```bash
./scripts/run_local.sh
```

Résultat attendu :

```text
OK: concept loaded -> Protein Coffee
OK: video brief created -> 20s 16:9
OK: benchmarks loaded -> 2 peer products
OK: RSP recommendation -> USD 2.96 (2.66-3.26)
OK: persona task created -> Busy US professional website_review
```

Puis tu dois aussi voir que `pytest` termine avec des tests qui passent.

## 3. Si le script n'est pas exécutable

Si ton terminal affiche une erreur de permission, lance :

```bash
chmod +x scripts/run_local.sh
./scripts/run_local.sh
```

## 4. Ce que tu peux modifier pour tester

### Concept produit

Ouvre ce fichier :

```text
examples/sample_concept.json
```

Change par exemple :

- `name`
- `description`
- `target_audience`
- `benefits`
- `reasons_to_believe`

Puis relance :

```bash
./scripts/run_local.sh
```

Tu dois voir le nouveau nom du concept dans la ligne :

```text
OK: concept loaded -> ...
```

### Produits benchmark et prix

Ouvre ce fichier :

```text
examples/sample_benchmark.json
```

Change par exemple :

- `price`
- `similarity_score`
- `claims`
- `format`

Puis relance :

```bash
./scripts/run_local.sh
```

Tu dois voir la recommandation RSP changer dans la ligne :

```text
OK: RSP recommendation -> ...
```

## 5. Ce qui existe aujourd'hui

Aujourd'hui, le projet sait :

- charger un concept produit depuis JSON ;
- charger des produits benchmarks depuis JSON ;
- créer un brief vidéo structuré ;
- calculer une recommandation RSP simple à partir des prix et scores de similarité ;
- créer une tâche pour un agent persona ;
- vérifier tout ça avec des tests automatisés.

## 6. Ce qui n'existe pas encore

Le projet ne fait pas encore :

- génération réelle de vidéo marketing ;
- scraping live de prix retailer ;
- pilotage d'un navigateur par une persona ;
- interface web utilisateur.

Ces parties sont les prochaines étapes à construire au-dessus de cette base.
