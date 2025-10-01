# Discord Rei Bot  

A Discord bot powered by a flexible **magi command system**, automatic migrations, and hot-reloading support.  

## ✨ Features  

- **🧩 Magi Commands (CLI Tool)**  
  The `magi` tool helps you manage everything from database migrations to models and cogs:  

  | Command                  | Description |
  |--------------------------|-------------|
  | `magi migrate`           | Run all pending migrations |
  | `magi migration:make`    | Create a new table migration |
  | `magi migration:add`     | Add new columns to a table |
  | `magi migration:modify`  | Modify existing columns |
  | `magi migration:remove`  | Remove columns |
  | `magi model:make`        | Create a new model (with fillable fields + migrations) |
  | `magi cog:make`          | Generate a new Cog with slash/classic commands, also allows you to use AI for commands creation |

- **📦 Database Migrations**  
  No need to write raw SQL — migrations are generated automatically through interactive prompts.  

- **🔗 ORM Support**  
  Uses [Orator](https://github.com/sdispater/orator/) (Eloquent-like ORM). Work with your database through clean Python models.  

- **♻️ Hot Reloading**  
  Update your code in real time. The bot reloads changes instantly without restarts.  

- **⚙️ Cog System**  
  Works with both classic (`!command`) and slash (`/command`) commands. Supports normal Cogs and GroupCogs, without setup command!  

- **🤖 AI Rei Cog**  
  Includes a Cog where the bot roleplays as **Ayanami Rei** from *Neon Genesis Evangelion*.  

## 🚀 Live Demo  
All commits to the `main` branch are automatically applied to the bot running on my [Discord Server](https://discord.gg/tUZzEH5H9U).  
You can play with it live — just make a commit, I’ll review & merge, and the bot updates itself.  

---
