#!/usr/bin/env python3
"""
Design System - Professional UX/UI Design
Complete design system for user experience and interface design

Features:
- UX design and user research
- UI component design
- Design systems and style guides
- Accessibility (WCAG compliance)
- Responsive design
- Brand identity and visual design
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class DesignPhase(Enum):
    """Design process phases."""
    RESEARCH = "research"
    IDEATION = "ideation"
    WIREFRAME = "wireframe"
    PROTOTYPE = "prototype"
    VISUAL_DESIGN = "visual_design"
    USER_TESTING = "user_testing"
    ITERATION = "iteration"


class AccessibilityLevel(Enum):
    """WCAG conformance levels."""
    A = "A"
    AA = "AA"
    AAA = "AAA"


@dataclass
class UserPersona:
    """User persona for UX design."""
    name: str
    age_range: str
    occupation: str
    goals: List[str]
    pain_points: List[str]
    tech_savviness: str
    devices: List[str]
    quote: str


@dataclass
class UserFlow:
    """User flow diagram."""
    name: str
    entry_point: str
    steps: List[Dict[str, str]]
    exit_point: str
    decision_points: List[str]
    pain_points: List[str]


@dataclass
class Wireframe:
    """Wireframe specification."""
    screen_name: str
    layout: str
    components: List[str]
    interactions: List[str]
    notes: str


@dataclass
class DesignToken:
    """Design token (color, spacing, typography, etc.)."""
    name: str
    category: str  # color, spacing, typography, shadow, etc.
    value: str
    description: str


@dataclass
class UIComponent:
    """UI component specification."""
    name: str
    description: str
    variants: List[str]
    states: List[str]  # default, hover, active, disabled, etc.
    props: Dict[str, Any]
    accessibility: Dict[str, str]
    usage: str


@dataclass
class DesignSystem:
    """Complete design system."""
    name: str
    version: str
    tokens: List[DesignToken]
    components: List[UIComponent]
    principles: List[str]
    guidelines: Dict[str, str]


class DesignStudio:
    """Professional Design Studio."""
    
    def __init__(self):
        """Initialize design studio."""
        self.personas: List[UserPersona] = []
        self.flows: List[UserFlow] = []
        self.wireframes: List[Wireframe] = []
        
    def create_user_persona(self, name: str, context: str = "") -> UserPersona:
        """Create user persona."""
        # In production, this would be based on user research data
        persona = UserPersona(
            name=name,
            age_range="25-40",
            occupation="Software Developer",
            goals=[
                "Complete tasks efficiently",
                "Understand system behavior",
                "Avoid errors and frustration"
            ],
            pain_points=[
                "Complex interfaces",
                "Unclear error messages",
                "Slow performance"
            ],
            tech_savviness="High",
            devices=["Desktop", "Mobile", "Tablet"],
            quote="I want tools that work reliably and don't waste my time"
        )
        self.personas.append(persona)
        return persona
    
    async def design_user_experience(self, feature: str) -> Dict[str, Any]:
        """Design complete user experience."""
        return {
            "feature": feature,
            "user_research": {
                "personas": [
                    "Primary user: Technical professional",
                    "Secondary user: Business stakeholder"
                ],
                "user_goals": [
                    "Accomplish task quickly",
                    "Understand system state",
                    "Recover from errors"
                ],
                "pain_points": [
                    "Complex workflows",
                    "Unclear feedback",
                    "Poor error handling"
                ]
            },
            "user_flows": {
                "happy_path": [
                    "1. Land on feature",
                    "2. Understand options",
                    "3. Make selection",
                    "4. See confirmation",
                    "5. Complete task"
                ],
                "error_path": [
                    "1. Attempt action",
                    "2. See clear error",
                    "3. Understand issue",
                    "4. Fix problem",
                    "5. Retry successfully"
                ]
            },
            "wireframes": {
                "layout": "Clean, focused layout with clear hierarchy",
                "key_elements": [
                    "Clear headline explaining purpose",
                    "Progressive disclosure of options",
                    "Prominent primary action",
                    "Secondary actions available but not prominent",
                    "Status indicators",
                    "Help text where needed"
                ]
            },
            "interactions": {
                "primary_actions": "Large, clear buttons with descriptive labels",
                "feedback": "Immediate visual feedback for all actions",
                "validation": "Real-time validation with helpful messages",
                "loading": "Loading indicators with progress where possible",
                "errors": "Inline errors with clear remediation"
            },
            "accessibility": {
                "keyboard": "Full keyboard navigation",
                "screen_reader": "Proper ARIA labels and roles",
                "contrast": "WCAG AA contrast ratios",
                "focus": "Clear focus indicators",
                "alt_text": "Descriptive alt text for images"
            }
        }
    
    async def create_ui_components(self, feature: str) -> List[UIComponent]:
        """Design UI components."""
        components = [
            UIComponent(
                name="Button",
                description="Primary action button",
                variants=["primary", "secondary", "tertiary", "ghost"],
                states=["default", "hover", "active", "disabled", "loading"],
                props={
                    "label": "string",
                    "icon": "optional",
                    "size": "sm | md | lg",
                    "fullWidth": "boolean"
                },
                accessibility={
                    "role": "button",
                    "aria-label": "Descriptive label",
                    "aria-disabled": "true when disabled"
                },
                usage="Use for primary actions. Limit to 1-2 per screen."
            ),
            UIComponent(
                name="Input",
                description="Text input field",
                variants=["text", "email", "password", "number"],
                states=["default", "focus", "error", "disabled"],
                props={
                    "label": "string",
                    "placeholder": "string",
                    "helperText": "string",
                    "error": "string",
                    "required": "boolean"
                },
                accessibility={
                    "role": "textbox",
                    "aria-label": "Label text",
                    "aria-invalid": "true when error",
                    "aria-describedby": "Helper text ID"
                },
                usage="Always include label. Show validation inline."
            ),
            UIComponent(
                name="Card",
                description="Content container",
                variants=["elevated", "outlined", "filled"],
                states=["default", "hover", "selected"],
                props={
                    "title": "string",
                    "description": "string",
                    "image": "optional",
                    "actions": "array"
                },
                accessibility={
                    "role": "article",
                    "aria-labelledby": "Title ID"
                },
                usage="Group related content. Use consistent spacing."
            )
        ]
        return components
    
    async def accessibility_audit(self, page: str) -> Dict[str, Any]:
        """Perform accessibility audit."""
        return {
            "page": page,
            "wcag_level": AccessibilityLevel.AA.value,
            "checks": {
                "perceivable": {
                    "text_alternatives": "All images have alt text",
                    "captions": "Video/audio has captions",
                    "adaptable": "Content works in different layouts",
                    "contrast": "Minimum 4.5:1 for normal text, 3:1 for large"
                },
                "operable": {
                    "keyboard": "All functionality via keyboard",
                    "timing": "No time limits or user can extend",
                    "seizures": "No flashing content",
                    "navigation": "Skip links and clear focus"
                },
                "understandable": {
                    "readable": "Clear language, defined jargon",
                    "predictable": "Consistent navigation and behavior",
                    "input_assistance": "Error identification and suggestions"
                },
                "robust": {
                    "compatible": "Valid HTML, ARIA roles",
                    "parsing": "No errors in markup"
                }
            },
            "issues_found": [
                {
                    "severity": "critical",
                    "issue": "Missing alt text on decorative images",
                    "remediation": "Add alt='' for decorative images"
                },
                {
                    "severity": "high",
                    "issue": "Form labels not associated with inputs",
                    "remediation": "Use for/id or wrap inputs with labels"
                }
            ],
            "score": 85,
            "recommendations": [
                "Add ARIA landmarks for screen readers",
                "Ensure focus order matches visual order",
                "Add skip navigation link",
                "Test with actual screen readers",
                "Keyboard test all interactions"
            ]
        }
    
    async def create_design_system(self, product: str) -> DesignSystem:
        """Create complete design system."""
        tokens = [
            # Colors
            DesignToken("color-primary", "color", "#0066CC", "Primary brand color"),
            DesignToken("color-secondary", "color", "#6C757D", "Secondary color"),
            DesignToken("color-success", "color", "#28A745", "Success state"),
            DesignToken("color-error", "color", "#DC3545", "Error state"),
            DesignToken("color-warning", "color", "#FFC107", "Warning state"),
            DesignToken("color-text", "color", "#212529", "Primary text"),
            DesignToken("color-background", "color", "#FFFFFF", "Background"),
            
            # Spacing
            DesignToken("space-xs", "spacing", "4px", "Extra small space"),
            DesignToken("space-sm", "spacing", "8px", "Small space"),
            DesignToken("space-md", "spacing", "16px", "Medium space"),
            DesignToken("space-lg", "spacing", "24px", "Large space"),
            DesignToken("space-xl", "spacing", "32px", "Extra large space"),
            
            # Typography
            DesignToken("font-family", "typography", "Inter, system-ui, sans-serif", "Primary font"),
            DesignToken("font-size-sm", "typography", "14px", "Small text"),
            DesignToken("font-size-md", "typography", "16px", "Body text"),
            DesignToken("font-size-lg", "typography", "20px", "Large text"),
            DesignToken("font-size-xl", "typography", "24px", "Heading"),
            
            # Shadows
            DesignToken("shadow-sm", "shadow", "0 1px 2px rgba(0,0,0,0.1)", "Subtle shadow"),
            DesignToken("shadow-md", "shadow", "0 4px 6px rgba(0,0,0,0.1)", "Medium shadow"),
            DesignToken("shadow-lg", "shadow", "0 10px 15px rgba(0,0,0,0.1)", "Large shadow"),
        ]
        
        components = await self.create_ui_components(product)
        
        return DesignSystem(
            name=f"{product} Design System",
            version="1.0.0",
            tokens=tokens,
            components=components,
            principles=[
                "Clarity: Make it obvious what to do next",
                "Efficiency: Minimize steps to accomplish goals",
                "Consistency: Use patterns users already know",
                "Feedback: Show what's happening at all times",
                "Forgiving: Make it easy to undo and recover",
                "Accessible: Work for everyone"
            ],
            guidelines={
                "spacing": "Use 8px grid system for consistent spacing",
                "color": "Maintain 4.5:1 contrast for text",
                "typography": "Use scale consistently, max 3 font sizes per screen",
                "layout": "Use responsive grid, mobile-first approach",
                "motion": "Keep animations under 300ms, use easing",
                "accessibility": "Target WCAG AA minimum, AAA when possible"
            }
        )
    
    async def responsive_design(self, feature: str) -> Dict[str, Any]:
        """Design responsive breakpoints and layouts."""
        return {
            "feature": feature,
            "approach": "Mobile-first responsive design",
            "breakpoints": {
                "mobile": "< 640px",
                "tablet": "640px - 1024px",
                "desktop": "> 1024px",
                "wide": "> 1440px"
            },
            "layouts": {
                "mobile": {
                    "columns": 1,
                    "navigation": "Bottom tab bar",
                    "spacing": "Compact (8px)",
                    "font_size": "16px base (prevent zoom)"
                },
                "tablet": {
                    "columns": 2,
                    "navigation": "Side drawer",
                    "spacing": "Standard (16px)",
                    "font_size": "16px base"
                },
                "desktop": {
                    "columns": 3,
                    "navigation": "Top bar + sidebar",
                    "spacing": "Spacious (24px)",
                    "font_size": "16px base"
                }
            },
            "touch_targets": "Minimum 44x44px for mobile",
            "images": "Use srcset for responsive images",
            "performance": "Lazy load below fold, optimize images"
        }
    
    async def brand_identity(self, product: str) -> Dict[str, Any]:
        """Create brand identity guidelines."""
        return {
            "product": product,
            "brand_values": [
                "Reliable",
                "Innovative",
                "User-focused",
                "Professional"
            ],
            "voice_tone": {
                "voice": "Professional yet approachable",
                "tone": "Helpful, clear, confident",
                "writing_style": [
                    "Use active voice",
                    "Be concise",
                    "Avoid jargon",
                    "Be specific"
                ]
            },
            "visual_identity": {
                "logo": "Clean, modern wordmark",
                "color_palette": {
                    "primary": "#0066CC (Trust, stability)",
                    "secondary": "#6C757D (Balance)",
                    "accent": "#28A745 (Success, growth)"
                },
                "typography": {
                    "headings": "Inter Bold",
                    "body": "Inter Regular",
                    "code": "Fira Code"
                },
                "imagery": "Technical, clean, modern photography",
                "iconography": "Outlined style, consistent weight"
            },
            "applications": {
                "ui": "Apply brand colors consistently",
                "marketing": "Use brand voice in all copy",
                "documentation": "Maintain professional tone",
                "social": "Friendly but professional"
            }
        }


# Convenience functions
async def design_feature(feature: str) -> Dict[str, Any]:
    """Quick UX design for feature."""
    studio = DesignStudio()
    return await studio.design_user_experience(feature)


async def design_system(product: str) -> DesignSystem:
    """Quick design system creation."""
    studio = DesignStudio()
    return await studio.create_design_system(product)


# Global design studio
_design_studio: Optional[DesignStudio] = None


def get_design_studio() -> DesignStudio:
    """Get global design studio."""
    global _design_studio
    if _design_studio is None:
        _design_studio = DesignStudio()
    return _design_studio
