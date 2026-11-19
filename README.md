# Estructuras de Datos y Algoritmos en Python 🧠🐍

Repositorio con los **4 proyectos (Retos)** desarrollados en **Python** para el curso **ISIS-1225 — Estructuras de Datos y Algoritmos** (Universidad de los Andes).

Cada reto sigue una **arquitectura MVC** (`App/model.py`, `App/controller.py`, `App/view.py`) y resuelve problemas de análisis de datos sobre datasets reales (Spotify, FIFA 2022 y Toronto BikeShare) evaluando complejidad temporal y espacial con `time` y `tracemalloc`.

---

## 🛠️ Competencias y Algoritmos Implementados

- **Arquitectura y Buenas Prácticas:** patrón Modelo-Vista-Controlador (MVC), modularización, pruebas unitarias y medición empírica de tiempo y memoria (`time`, `tracemalloc`).
- **Estructuras Lineales y Ordenamientos:** `ArrayList`, `SingleLinked`, `Stack`, `InsertionSort`, `SelectionSort`, `ShellSort`, `MergeSort` y `QuickSort`.
- **Tablas de Hash (Mapas):** manejo de colisiones con *Separate Chaining* y *Linear Probing*, ajuste de factor de carga y optimización de búsquedas $O(1)$ promedio.
- **Árboles Ordenados:** Árboles Binarios de Búsqueda (**BST**) y Árboles Rojo-Negro (**RBT**) para consultas eficientes por rangos.
- **Grafos y Rutas:** grafos dirigidos ponderados, recorridos **BFS** / **DFS**, caminos mínimos con **Dijkstra** y componentes fuertemente conectados (**Kosaraju SCC**).

---

## ⭐ Proyectos (Retos)

| Reto | Dominio / Dataset | Estructuras y Algoritmos | Informe de Análisis |
| :---: | :--- | :--- | :---: |
| [**Reto 1**](reto-1-spotify-listas-ordenamientos/) | **Spotify** (álbumes, artistas y tracks) | `ArrayList`, `SingleLinked`, `Insertion`, `Selection`, `Shell`, `MergeSort`, `QuickSort` | [PDF](reto-1-spotify-listas-ordenamientos/Docs/analisis-reto-1.pdf) |
| [**Reto 2**](reto-2-spotify-tablas-hash/) | **Spotify** (optimización de consultas) | Tablas de Hash (`Separate Chaining`, `Linear Probing`), benchmarking de memoria y tiempo | [PDF](reto-2-spotify-tablas-hash/Docs/analisis-reto-2.pdf) |
| [**Reto 3**](reto-3-fifa-arboles-bst-rbt/) | **FIFA 2022 Players** (estadísticas y filtros) | Árboles Ordenados (**BST** y **Red-Black Tree**), consultas por rangos de edad/potencial/fechas | — |
| [**Reto 4**](reto-4-bikeshare-grafos/) | **Toronto BikeShare** (red de viajes) | Grafos dirigidos ponderados, **BFS**, **DFS**, **Dijkstra**, **Kosaraju SCC** | [PDF](reto-4-bikeshare-grafos/Docs/observaciones-reto-4.pdf) |

---

## 📂 Estructura del Repositorio

```text
estructuras-datos-algoritmos-python/
├── reto-1-spotify-listas-ordenamientos/
│   ├── App/            # model.py, controller.py, view.py, config.py
│   ├── Data/Spotify/   # Datasets de muestra (-small.csv)
│   ├── DISClib/        # Implementación de ADTs y algoritmos
│   ├── Docs/           # Informe de análisis de complejidad
│   └── Test/           # Pruebas unitarias de estructuras
│
├── reto-2-spotify-tablas-hash/
│   ├── App/
│   ├── Data/Spotify/   # Datasets de muestra (-small.csv)
│   ├── DISClib/
│   ├── Docs/           # Informe comparativo de tablas de hash
│   └── Test/
│
├── reto-3-fifa-arboles-bst-rbt/
│   ├── App/
│   ├── Data/FIFA/      # fifa-players-2022-utf8-small.csv
│   ├── DISClib/
│   └── Test/
│
├── reto-4-bikeshare-grafos/
│   ├── App/
│   ├── Data/           # Instrucciones para cargar datasets de BikeShare
│   ├── DISClib/
│   ├── Docs/           # Observaciones y análisis del Reto 4
│   └── Test/
│
├── requirements.txt
└── README.md
```

> **Nota sobre los datasets:** Para mantener el repositorio liviano dentro de los límites de GitHub, se incluyeron únicamente los archivos de muestra (`*-small.csv`). Los datasets completos (`large`, `80pct`, etc.) se excluyen mediante `.gitignore` y pueden colocarse en la carpeta `Data/` de cada reto.

---

## 🚀 Cómo ejecutar cada Reto

### 1. Clonar el repositorio e instalar dependencias

```bash
git clone https://github.com/Wsux-Moonbow/estructuras-datos-algoritmos-python.git
cd estructuras-datos-algoritmos-python
pip install -r requirements.txt
```

### 2. Ejecutar la consola interactiva (MVC) de cualquier reto

```bash
# Reto 1 - Spotify (Listas y Ordenamientos)
cd reto-1-spotify-listas-ordenamientos
python App/view.py

# Reto 2 - Spotify (Tablas de Hash)
cd reto-2-spotify-tablas-hash
python App/view.py

# Reto 3 - FIFA 2022 (Árboles BST y RBT)
cd reto-3-fifa-arboles-bst-rbt
python App/view.py

# Reto 4 - BikeShare (Grafos)
cd reto-4-bikeshare-grafos
python App/view.py
```
