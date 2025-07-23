from kaggle_secrets import UserSecretsClient
import os
import subprocess

def run_git_cmd(args, check=True, capture=False):
    return subprocess.run(
        ["git"] + args,
        check=check,
        capture_output=capture,
        text=True
    )

def push_to_git_from_kaggle(repo_name: str, repo_path: str, commit_message: str = "Commit from Kaggle") -> str:
    original_dir = os.getcwd()
    os.chdir(repo_path)

    try:
        # Load GitHub secrets
        user_secrets = UserSecretsClient()
        username = user_secrets.get_secret("GITHUB_USERNAME")
        token = user_secrets.get_secret("GITHUB_TOKEN")
        remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

        # Git setup
        run_git_cmd(["add", "."], check=True)
        run_git_cmd(["commit", "-m", commit_message], check=False)
        run_git_cmd(["branch", "-M", "main"], check=False)
        run_git_cmd(["remote", "set-url", "origin", remote_url], check=False)
        run_git_cmd(["fetch", "origin"], check=True)

        # Check if remote is ahead
        rev_list = run_git_cmd(
            ["rev-list", "main..origin/main", "--count"],
            check=True, capture=True
        ).stdout.strip()

        if rev_list != "0":
            run_git_cmd(["pull", "--rebase", "origin", "main"], check=True)

        # Push to GitHub
        run_git_cmd(["push", "-u", "origin", "main"], check=True)

        return f"✅ Successfully pushed to https://github.com/{username}/{repo_name}"

    except subprocess.CalledProcessError as e:
        return f"❌ Git command failed: {e}"
    except Exception as e:
        return f"❌ Error: {e}"
    finally:
        os.chdir(original_dir)
     
