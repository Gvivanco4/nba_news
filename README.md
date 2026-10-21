# NBA Daily Newsletter

Genera un newsletter HTML con juegos, transacciones, estadísticas y noticias de la NBA y lo envía por Gmail.

## Ejecución local

Requiere Python 3.12.

```bash
python -m venv venv
venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
```

Completa `.env` con tu clave de Anthropic, remitente, destinatario y contraseña de aplicación de Gmail. Ejecuta desde la raíz:

```bash
venv/bin/python src/main.py
```

## GitHub Actions

El workflow `.github/workflows/newsletter.yml` ejecuta el envío cada día a las 08:00 de Ciudad de México (14:00 UTC). GitHub puede retrasar ejecuciones programadas.

Configura estos secretos en **Settings → Secrets and variables → Actions → New repository secret**:

| Secreto | Valor |
| --- | --- |
| `ANTHROPIC_API_KEY` | Clave de Anthropic con acceso al modelo configurado en `src/llm_client.py`. |
| `SENDER_EMAIL` | Cuenta Gmail que envía el newsletter. |
| `RECEIPT_EMAIL` | Correo destinatario. |
| `GMAIL_APP_PASSWORD` | Contraseña de aplicación de Gmail del remitente. |

En **Actions → NBA Daily Newsletter → Run workflow** puedes iniciar un envío manual. El workflow debe estar en la rama predeterminada para ejecutar la programación. No subas archivos `.env` ni credenciales al repositorio.

La aplicación conserva compatibilidad con `CONTRASEÑA_GMAIL` para instalaciones locales existentes.
