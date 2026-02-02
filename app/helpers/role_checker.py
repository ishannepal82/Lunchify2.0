from fastapi import Depends, HTTPException, Request, status

def require_role(*allowed_roles: str):
    def checker(request: Request):
        actor = getattr(request.state, "actor", None)

        if not actor or actor["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )

        return actor
    return checker
