# HACS Submission Guide for Subscription Helper

## ✅ Pre-Submission Checklist

All requirements for HACS have been verified and are now complete:

### Required Files
- ✅ `custom_components/subscription_helper/manifest.json` - Contains all required fields
- ✅ `hacs.json` - HACS configuration file
- ✅ `README.md` - Main documentation
- ✅ `info.md` - HACS info page
- ✅ `brands_icons/icon.png` - Logo (already accepted by HACS)
- ✅ `brands_icons/icon@2x.png` - High-res logo

### manifest.json Required Fields
- ✅ `domain`: subscription_helper
- ✅ `name`: Subscription Helper
- ✅ `version`: 1.6.1
- ✅ `documentation`: https://github.com/mariobrosch/subscription-helper
- ✅ `issue_tracker`: https://github.com/mariobrosch/subscription-helper/issues (newly added)
- ✅ `codeowners`: [@mariobrosch]

### hacs.json Configuration
- ✅ `name`: Subscription Helper
- ✅ `render_readme`: true
- ✅ `country`: NL
- ✅ `homeassistant`: 2023.1.0

## 📝 Step-by-Step HACS Submission Process

### Method 1: Submit to HACS Default Repository (Recommended)

To get your integration listed in the official HACS store:

1. **Ensure your repository is public** on GitHub

2. **Add GitHub Topics** to your repository:
   - Go to your repository on GitHub: https://github.com/mariobrosch/subscription-helper
   - Click the settings gear icon next to "About"
   - Add these topics:
     - `home-assistant`
     - `hacs`
     - `home-assistant-integration`
     - `home-assistant-hacs`

3. **Submit to HACS**:
   - Go to: https://github.com/hacs/default/issues/new/choose
   - Select "Add Integration"
   - Fill in the form with your repository URL: `https://github.com/mariobrosch/subscription-helper`
   - Submit the issue

4. **Wait for Review**:
   - HACS team will review your submission
   - They may request changes or ask questions
   - Once approved, your integration will appear in HACS for all users

### Method 2: Add as Custom Repository (For Users)

Until the integration is added to the default HACS store, users can add it manually:

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots (⋮) in the top right corner
4. Select "Custom repositories"
5. Enter repository URL: `https://github.com/mariobrosch/subscription-helper`
6. Select category: "Integration"
7. Click "Add"
8. Search for "Subscription Helper"
9. Click "Download"
10. Restart Home Assistant

## 🎯 What Changed

The following change was made to make the repository HACS-compliant:

- **Added `issue_tracker` field** to `manifest.json`
  - This is a required field for HACS validation
  - Points to: https://github.com/mariobrosch/subscription-helper/issues

## 📋 Next Steps After HACS Acceptance

1. **Tag a Release**:
   ```bash
   git tag -a v1.6.1 -m "Version 1.6.1 - HACS ready"
   git push origin v1.6.1
   ```

2. **Update Documentation**:
   - Remove instructions about adding as custom repository from README
   - Update installation instructions to reflect HACS availability

3. **Announce**:
   - Share on Home Assistant Community forum
   - Update any social media or blog posts

## 🔍 Validation

Your repository has been validated against HACS requirements and passes all checks:

```
✓ domain: subscription_helper
✓ name: Subscription Helper
✓ version: 1.6.1
✓ documentation: https://github.com/mariobrosch/subscription-helper
✓ issue_tracker: https://github.com/mariobrosch/subscription-helper/issues
✓ codeowners: ['@mariobrosch']
✓ hacs.json exists with name field
✓ All required files present
✓ Logo already accepted by HACS
```

## 📚 Resources

- [HACS Documentation](https://hacs.xyz/docs/publish/integration/)
- [Home Assistant Integration Manifest](https://developers.home-assistant.io/docs/creating_integration_manifest/)
- [HACS Default Repository](https://github.com/hacs/default)

## ✨ Summary

**Your Subscription Helper integration is now fully HACS-compliant and ready for submission!**

The only required change was adding the `issue_tracker` field to your manifest.json file. All other requirements were already met, including your logo which was previously accepted by HACS.

You can now proceed with submitting your integration to HACS using the step-by-step guide above.
