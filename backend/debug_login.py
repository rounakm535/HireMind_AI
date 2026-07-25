"""
Debug script to diagnose the login issue.
Run from the backend directory: python debug_login.py
"""
import asyncio
import sys
import os

async def main():
    print("Step 1: Importing models...")
    try:
        from app.db.database import AsyncSessionLocal, init_db, Base
        import app.models.user
        import app.models.organization
        print("  OK: Models imported")
    except Exception as e:
        print(f"  FAIL: Model import failed: {e}")
        return

    print("\nStep 2: Initializing database...")
    try:
        await init_db()
        print("  OK: DB initialized")
    except Exception as e:
        print(f"  FAIL: DB init failed: {e}")
        return

    print("\nStep 3: Querying user by email...")
    try:
        from sqlalchemy import select
        from app.models.user import User
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.email == "mishra.rounak15@gmail.com")
            )
            user = result.scalars().first()
            if user:
                print(f"  OK: User found: id={user.id}, email={user.email}, is_active={user.is_active}")
                print(f"  OK: Hash starts with: {user.hashed_password[:20]}...")
            else:
                print("  FAIL: User NOT found in DB!")
                print("\n  Listing all users:")
                all_result = await session.execute(select(User))
                all_users = all_result.scalars().all()
                if all_users:
                    for u in all_users:
                        print(f"    - {u.email} (active={u.is_active})")
                else:
                    print("    (no users in database)")
                print("\nCreating new user mishra.rounak15@gmail.com with password Admin@1234 ...")
                from app.core.security import get_password_hash
                from app.models.user import User, UserRole
                new_user = User(
                    email="mishra.rounak15@gmail.com",
                    hashed_password=get_password_hash("Admin@1234"),
                    first_name="Rounak",
                    last_name="Mishra",
                    role=UserRole.ADMIN,
                    is_active=True,
                )
                async with AsyncSessionLocal() as s2:
                    s2.add(new_user)
                    await s2.commit()
                print("  OK: New user created. Login with Admin@1234")
                return
    except Exception as e:
        print(f"  FAIL: DB query failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\nStep 4: Resetting password to 'Admin@1234' and ensuring user is active...")
    try:
        from app.core.security import get_password_hash
        from sqlalchemy import update
        from app.models.user import User
        new_hash = get_password_hash("Admin@1234")
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(User)
                .where(User.email == "mishra.rounak15@gmail.com")
                .values(hashed_password=new_hash, is_active=True)
            )
            await session.commit()
        print("  OK: Password reset to 'Admin@1234' and user set to active")
    except Exception as e:
        print(f"  FAIL: Password reset failed: {e}")
        import traceback
        traceback.print_exc()

    print("\nStep 5: Verifying password works now...")
    try:
        from app.core.security import verify_password
        from sqlalchemy import select
        from app.models.user import User
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.email == "mishra.rounak15@gmail.com")
            )
            user = result.scalars().first()
            ok = verify_password("Admin@1234", user.hashed_password)
            print(f"  Verify result: {ok}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\nDone. Try logging in with: mishra.rounak15@gmail.com / Admin@1234")

if __name__ == "__main__":
    asyncio.run(main())
