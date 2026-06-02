# API — Auth

| Method | Path | Auth | Body | Response |
|--------|------|------|------|----------|
| POST | `/api/auth/signup` | no | `{ email, password }` | 201 `TokenResponse` |
| POST | `/api/auth/login` | no | `{ email, password }` | 200 `TokenResponse` |
| GET | `/api/auth/me` | yes | — | 200 `UserOut` |

**Service:** `AuthService` · **Repo:** `UserRepository`

**Affects if changed:** all protected routes, `api/deps.get_current_user_id`, frontend `AuthContext`
