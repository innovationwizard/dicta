# Design System: Swiss International Style

## Overview

The app has been redesigned following the **Swiss International Style** (also known as Swiss Typography or International Typographic Style) - a minimalist, grid-based design philosophy that prioritizes clarity, readability, and functionality.

## Design Principles

### Swiss Editorial Approach
- **Strict, High-Clarity**: Mimics a high-end document editor
- **Typography-First**: Emphasis on readable, clean fonts
- **Grid-Based Layout**: Structured, organized content
- **Minimalist**: No decorative elements, pure function
- **Professional**: Corporate, reliable aesthetic

## Color Palette

### Primary Colors

- **Background**: `#FFFFFF` (White)
- **Surface**: `#F3F4F6` (Gray 100) - For sidebars, toolbars, panels
- **Primary Text**: `#111827` (Gray 900) - Near black for maximum readability
- **Accent Color**: `#000000` (Black) - Used for primary buttons and key elements

### Functional Colors

- **Highlight/Selection**: `#FEF3C7` (Amber 100) - Classic highlighter look
- **Recording Indicator**: `#DC2626` (Red 600) - For error states and alerts
- **Border**: `#E5E7EB` (Gray 200) - Subtle separators
- **Secondary Text**: `#6B7280` (Gray 500)
- **Tertiary Text**: `#9CA3AF` (Gray 400)

## Typography

### Font Stack

**Primary**: Inter
- Clean, modern sans-serif
- Excellent readability at all sizes
- Professional and corporate-friendly

**Fallback**: System fonts
- -apple-system (macOS)
- BlinkMacSystemFont (macOS)
- Segoe UI (Windows)
- Roboto (Android)

### Typography Hierarchy

- **H1**: 28px, weight 600, uppercase, letter-spacing 0.05em
- **H2**: 13px, weight 600, uppercase, letter-spacing 0.1em
- **H3**: 11px, weight 600, uppercase, letter-spacing 0.1em
- **Body**: 14px, weight 400, line-height 1.8
- **Small**: 11-12px, weight 400
- **Labels**: 13px, weight 500-600

### Typography Principles

- **High Contrast**: Near-black text on white for maximum readability
- **Uppercase Labels**: All section headers and labels are uppercase
- **Letter Spacing**: Increased letter-spacing for uppercase text
- **Line Height**: 1.6-1.8 for comfortable reading
- **No Decorative Fonts**: Clean, functional typography only

## Layout

### Grid System

- **Max Width**: 1200px container
- **Spacing**: Consistent 8px grid (16px, 24px, 32px, 48px)
- **Padding**: 48px on desktop, 24px on mobile
- **Gaps**: 12px, 16px, 20px, 24px for consistent spacing

### Structure

- **Header**: Fixed height, border-bottom separator
- **Main Content**: Grid-based sections
- **Cards/Panels**: White or gray surface, 1px borders
- **Buttons**: Grid layout, consistent spacing

## Components

### Buttons

**Primary Button** (Black):
- Background: `#000000`
- Text: White
- Hover: Invert (white background, black text)
- Border: 2px solid black
- Text: Uppercase, letter-spacing 0.1em

**Secondary Button**:
- Background: White
- Border: 1px solid black
- Hover: Black background, white text

**Disabled State**:
- Background: `#F3F4F6` (Gray 100)
- Text: `#9CA3AF` (Gray 400)
- Border: `#E5E7EB` (Gray 200)

### Inputs & Checkboxes

- Clean, minimal styling
- Black accent color
- High contrast borders
- Clear focus states (2px black outline)

### Status Indicators

- **Running**: Black dot (pulsing)
- **Starting**: Gray dot (spinning)
- **Offline**: Red dot
- Small, minimal indicators (8px)

### Cards & Panels

- White background (`#FFFFFF`)
- Gray surface (`#F3F4F6`) for secondary panels
- 1px borders (`#E5E7EB`)
- No shadows or gradients
- Clean, flat design

## Interactions

### Hover States

- Subtle transitions (0.15s ease)
- Invert colors for buttons
- Highlight background for cards
- Clear visual feedback

### Focus States

- 2px black outline
- 2px offset
- High contrast for accessibility

### Loading States

- Minimal spinners
- Black/gray colors
- Clear loading messages
- No distracting animations

## Accessibility

### High Contrast

- All text meets WCAG AAA standards
- Minimum 7:1 contrast ratio
- Near-black text on white
- Clear focus indicators

### Typography

- Large, readable font sizes
- Comfortable line-height (1.6-1.8)
- Clear hierarchy
- No decorative fonts

### Interactive Elements

- Large click targets (minimum 44px)
- Clear hover/focus states
- Descriptive labels
- Keyboard navigation support

## Implementation Notes

### No Decorative Elements

- ❌ No gradients
- ❌ No shadows (except minimal)
- ❌ No emojis in UI
- ❌ No rounded corners (except minimal)
- ❌ No decorative icons

### Grid-Based

- ✅ Strict grid system
- ✅ Consistent spacing
- ✅ Aligned elements
- ✅ Organized layout

### Professional

- ✅ Corporate color scheme
- ✅ Business-appropriate
- ✅ Clean and minimal
- ✅ High-quality typography

---

**Result**: A professional, reliable, high-contrast interface that prioritizes clarity and readability above all else.

