# Graph Report - devsoft-heron-web  (2026-09-05)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 19 nodes · 40 edges · 3 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f6ab6d4f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- app.py
- admin_testimonios
- get_db_connection

## God Nodes (most connected - your core abstractions)
1. `get_db_connection()` - 7 edges
2. `admin_testimonios()` - 4 edges
3. `aprobar_testimonio()` - 4 edges
4. `eliminar_testimonio()` - 4 edges
5. `login_required()` - 4 edges
6. `nuevo_testimonio()` - 3 edges
7. `testimonios_aprobados()` - 3 edges
8. `admin_login()` - 2 edges
9. `admin_logout()` - 2 edges
10. `ads_txt()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `admin_testimonios()` --calls--> `get_db_connection()`  [EXTRACTED]
  app.py → app.py  _Bridges community 1 → community 2_
- `admin_testimonios()` --references--> `route`  [EXTRACTED]
  app.py →   _Bridges community 1 → community 0_
- `nuevo_testimonio()` --references--> `route`  [EXTRACTED]
  app.py →   _Bridges community 2 → community 0_

## Import Cycles
- None detected.

## Communities (3 total, 0 thin omitted)

### Community 0 - "app.py"
Cohesion: 0.33
Nodes (10): admin_login(), admin_logout(), ads_txt(), beta(), descargas(), gestor_condominal(), mantpro(), politica() (+2 more)

### Community 1 - "admin_testimonios"
Cohesion: 0.50
Nodes (4): admin_testimonios(), aprobar_testimonio(), eliminar_testimonio(), login_required()

### Community 2 - "get_db_connection"
Cohesion: 0.50
Nodes (4): get_db_connection(), init_testimonios_table(), nuevo_testimonio(), testimonios_aprobados()

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_db_connection()` connect `get_db_connection` to `app.py`, `admin_testimonios`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `admin_testimonios()` connect `admin_testimonios` to `app.py`, `get_db_connection`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Why does `aprobar_testimonio()` connect `admin_testimonios` to `app.py`, `get_db_connection`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._