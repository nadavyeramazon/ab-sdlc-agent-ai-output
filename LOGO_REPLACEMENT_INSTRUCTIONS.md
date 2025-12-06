# SwiftPay Logo Replacement Instructions

## Overview
The SwiftPay rebranding requires replacing the logo file. Due to tooling limitations with binary files, this step must be completed manually.

## Required Action

Replace `frontend/src/assets/logo.png` with the content from `frontend/src/assets/logo-swiftpay.png`

## Step-by-Step Instructions

### Option 1: Using Command Line (Recommended)

**On macOS/Linux:**
```bash
cd frontend/src/assets
cp logo-swiftpay.png logo.png
```

**On Windows (Command Prompt):**
```cmd
cd frontend\src\assets
copy logo-swiftpay.png logo.png
```

**On Windows (PowerShell):**
```powershell
cd frontend\src\assets
Copy-Item logo-swiftpay.png logo.png
```

### Option 2: Using File Explorer/Finder

1. Navigate to `frontend/src/assets/` directory
2. Find the file `logo-swiftpay.png`
3. Copy `logo-swiftpay.png`
4. Paste it in the same directory and rename to `logo.png` (overwrite existing)

### Option 3: Using Git

```bash
cd frontend/src/assets
git mv logo.png logo-old.png           # Backup old logo
cp logo-swiftpay.png logo.png          # Copy SwiftPay logo
git add logo.png
git commit -m "chore: Replace logo with SwiftPay branding"
```

## Verification

After replacement, verify the logo has been updated:

1. **Check file size:**
   - Old logo: ~8-10 KB
   - SwiftPay logo: ~2-3 KB

2. **Visual verification:**
   - Run the frontend: `npm run dev`
   - Open http://localhost:3000
   - The logo should show "SwiftPay" text on green background

3. **Check with Git:**
   ```bash
   git status
   # Should show: modified: frontend/src/assets/logo.png
   ```

## Why This Manual Step?

The automated deployment tools cannot directly copy or manipulate binary files (like PNG images). While all code changes have been completed automatically, binary file operations require manual intervention.

## Completion Checklist

- [ ] Logo file copied from `logo-swiftpay.png` to `logo.png`
- [ ] Frontend displays SwiftPay logo when running
- [ ] Changes committed to git
- [ ] Ready to test complete rebranding

## Next Steps

After completing the logo replacement:

1. Run the application: `docker compose up`
2. Verify the SwiftPay branding:
   - Green theme colors (emerald-500 and emerald-600)
   - SwiftPay logo in header
   - Delete All button with danger styling
3. Run tests: `npm test`
4. Commit changes if not already committed

## Notes

- The `logo-swiftpay.png` file is the official SwiftPay logo
- The old logo has been backed up (can be restored from git history)
- All other rebranding changes (CSS, theme colors) are already complete
- This is the final step to complete the rebranding

## Support

If you encounter any issues with the logo replacement, please refer to the git history or contact the development team.
