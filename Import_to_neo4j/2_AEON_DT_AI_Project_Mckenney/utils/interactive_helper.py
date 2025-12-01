"""
Interactive classification helper with rich terminal UI.

Provides beautiful terminal-based UI for user-assisted document classification,
including sector, subsector, and document type selection with AI suggestions.
"""

from typing import List, Dict, Optional, Tuple, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich import box
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
from datetime import datetime


class InteractiveHelper:
    """Interactive helper for document classification with rich UI."""

    # Predefined options
    SECTORS = [
        "Operations and Maintenance",
        "Planning and Development",
        "Administrative and Financial",
        "Safety and Environmental",
        "Technical and Engineering",
        "Legal and Regulatory",
        "Quality Control",
        "Other"
    ]

    SUBSECTORS = {
        "Operations and Maintenance": [
            "Equipment Maintenance",
            "Facility Operations",
            "Preventive Maintenance",
            "Emergency Repairs",
            "Other"
        ],
        "Planning and Development": [
            "Strategic Planning",
            "Project Development",
            "Budget Planning",
            "Resource Allocation",
            "Other"
        ],
        "Administrative and Financial": [
            "Financial Reports",
            "Human Resources",
            "Procurement",
            "Contracts Management",
            "Other"
        ],
        "Safety and Environmental": [
            "Safety Protocols",
            "Environmental Compliance",
            "Incident Reports",
            "Risk Assessment",
            "Other"
        ],
        "Technical and Engineering": [
            "Technical Specifications",
            "Engineering Designs",
            "Systems Documentation",
            "Technical Standards",
            "Other"
        ],
        "Legal and Regulatory": [
            "Legal Documents",
            "Compliance Reports",
            "Regulatory Filings",
            "Policy Documents",
            "Other"
        ],
        "Quality Control": [
            "Quality Audits",
            "Inspection Reports",
            "Quality Standards",
            "Performance Metrics",
            "Other"
        ],
        "Other": [
            "Miscellaneous",
            "Uncategorized"
        ]
    }

    DOCUMENT_TYPES = [
        "Report",
        "Manual",
        "Specification",
        "Procedure",
        "Policy",
        "Contract",
        "Invoice",
        "Correspondence",
        "Drawing",
        "Other"
    ]

    def __init__(self, qdrant_client: Optional[QdrantClient] = None,
                 collection_name: str = "classification_corrections"):
        """Initialize interactive helper.

        Args:
            qdrant_client: Optional Qdrant client for tracking corrections
            collection_name: Collection name for storing user corrections
        """
        self.console = Console()
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name

        # Create collection if Qdrant client provided
        if self.qdrant_client:
            try:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config={"size": 1, "distance": "Cosine"}  # Minimal config
                )
            except Exception:
                pass  # Collection already exists

    def _show_document_preview(self, document_summary: str, max_chars: int = 500) -> None:
        """Display document preview in a panel.

        Args:
            document_summary: Document content to preview
            max_chars: Maximum characters to show
        """
        preview = document_summary[:max_chars]
        if len(document_summary) > max_chars:
            preview += "..."

        panel = Panel(
            preview,
            title="[bold cyan]Document Preview[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print(panel)
        self.console.print()

    def _show_suggestions(self, suggestions: List[Tuple[str, float]],
                         title: str = "AI Suggestions") -> None:
        """Display AI suggestions with confidence scores.

        Args:
            suggestions: List of (option, confidence) tuples
            title: Table title
        """
        table = Table(title=title, box=box.ROUNDED, border_style="green")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Option", style="yellow")
        table.add_column("Confidence", style="green", justify="right")

        for idx, (option, confidence) in enumerate(suggestions, 1):
            confidence_bar = self._confidence_bar(confidence)
            table.add_row(str(idx), option, confidence_bar)

        self.console.print(table)
        self.console.print()

    def _confidence_bar(self, confidence: float) -> str:
        """Create a visual confidence bar.

        Args:
            confidence: Confidence score (0.0 to 1.0)

        Returns:
            Formatted confidence bar string
        """
        percentage = int(confidence * 100)
        bar_length = 10
        filled = int(bar_length * confidence)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Color based on confidence
        if confidence >= 0.8:
            color = "green"
        elif confidence >= 0.6:
            color = "yellow"
        else:
            color = "red"

        return f"[{color}]{bar}[/{color}] {percentage}%"

    def _show_options_menu(self, options: List[str], title: str = "Available Options") -> None:
        """Display available options in a table.

        Args:
            options: List of options to display
            title: Table title
        """
        table = Table(title=title, box=box.ROUNDED, border_style="blue")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Option", style="white")

        for idx, option in enumerate(options, 1):
            table.add_row(str(idx), option)

        self.console.print(table)
        self.console.print()

    def _track_correction(self, correction_type: str, ai_suggestion: str,
                         user_choice: str, document_summary: str,
                         confidence: float) -> None:
        """Track user correction in Qdrant.

        Args:
            correction_type: Type of correction (sector, subsector, document_type)
            ai_suggestion: What AI suggested
            user_choice: What user selected
            document_summary: Document content
            confidence: AI confidence score
        """
        if not self.qdrant_client:
            return

        try:
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=[0.0],  # Minimal vector
                payload={
                    "correction_type": correction_type,
                    "ai_suggestion": ai_suggestion,
                    "user_choice": user_choice,
                    "document_summary": document_summary[:1000],
                    "confidence": confidence,
                    "was_corrected": ai_suggestion != user_choice,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not track correction: {e}[/yellow]")

    def ask_sector_classification(self, document_summary: str,
                                  suggested_sector: str,
                                  confidence: float) -> str:
        """Ask user to classify document sector.

        Args:
            document_summary: Document content preview
            suggested_sector: AI-suggested sector
            confidence: AI confidence score (0.0 to 1.0)

        Returns:
            User-selected sector
        """
        self.console.clear()
        self.console.print(Panel(
            "[bold green]Sector Classification[/bold green]",
            border_style="green",
            box=box.DOUBLE
        ))
        self.console.print()

        # Show document preview
        self._show_document_preview(document_summary)

        # Show AI suggestion
        self._show_suggestions(
            [(suggested_sector, confidence)],
            title="AI Suggested Sector"
        )

        # Ask user decision
        self.console.print("[bold]What would you like to do?[/bold]")
        self.console.print("1. Accept AI suggestion")
        self.console.print("2. Choose from all sectors")
        self.console.print("3. Enter custom sector")
        self.console.print()

        choice = Prompt.ask(
            "Your choice",
            choices=["1", "2", "3"],
            default="1"
        )

        result = None

        if choice == "1":
            result = suggested_sector
            self.console.print(f"[green]✓[/green] Accepted: {result}")

        elif choice == "2":
            self.console.print()
            self._show_options_menu(self.SECTORS, "Available Sectors")

            sector_choice = Prompt.ask(
                "Select sector number",
                choices=[str(i) for i in range(1, len(self.SECTORS) + 1)]
            )
            result = self.SECTORS[int(sector_choice) - 1]
            self.console.print(f"[green]✓[/green] Selected: {result}")

        else:  # choice == "3"
            result = Prompt.ask("\n[bold]Enter custom sector[/bold]")
            self.console.print(f"[green]✓[/green] Custom sector: {result}")

        # Track correction
        self._track_correction(
            "sector", suggested_sector, result,
            document_summary, confidence
        )

        self.console.print()
        return result

    def ask_subsector_classification(self, sector: str,
                                    document_summary: str,
                                    suggestions: List[Tuple[str, float]]) -> str:
        """Ask user to classify document subsector.

        Args:
            sector: Selected sector
            document_summary: Document content preview
            suggestions: List of (subsector, confidence) tuples

        Returns:
            User-selected subsector
        """
        self.console.clear()
        self.console.print(Panel(
            f"[bold blue]Subsector Classification for: {sector}[/bold blue]",
            border_style="blue",
            box=box.DOUBLE
        ))
        self.console.print()

        # Show document preview
        self._show_document_preview(document_summary)

        # Show AI suggestions
        if suggestions:
            self._show_suggestions(suggestions, "AI Suggested Subsectors")

        # Ask user decision
        self.console.print("[bold]What would you like to do?[/bold]")
        if suggestions:
            self.console.print("1. Accept top AI suggestion")
            self.console.print("2. Choose from AI suggestions")
            self.console.print("3. Choose from all subsectors")
            self.console.print("4. Enter custom subsector")
            choices = ["1", "2", "3", "4"]
        else:
            self.console.print("1. Choose from all subsectors")
            self.console.print("2. Enter custom subsector")
            choices = ["1", "2"]

        self.console.print()

        choice = Prompt.ask(
            "Your choice",
            choices=choices,
            default="1"
        )

        result = None
        top_suggestion = suggestions[0][0] if suggestions else None

        if suggestions and choice == "1":
            result = top_suggestion
            self.console.print(f"[green]✓[/green] Accepted: {result}")

        elif suggestions and choice == "2":
            self.console.print()
            for idx, (subsector, conf) in enumerate(suggestions, 1):
                self.console.print(f"{idx}. {subsector} ({self._confidence_bar(conf)})")

            subsector_choice = Prompt.ask(
                "\nSelect subsector number",
                choices=[str(i) for i in range(1, len(suggestions) + 1)]
            )
            result = suggestions[int(subsector_choice) - 1][0]
            self.console.print(f"[green]✓[/green] Selected: {result}")

        elif (suggestions and choice == "3") or (not suggestions and choice == "1"):
            # Show all subsectors for this sector
            subsectors = self.SUBSECTORS.get(sector, ["Other"])
            self.console.print()
            self._show_options_menu(subsectors, f"Subsectors in {sector}")

            subsector_choice = Prompt.ask(
                "Select subsector number",
                choices=[str(i) for i in range(1, len(subsectors) + 1)]
            )
            result = subsectors[int(subsector_choice) - 1]
            self.console.print(f"[green]✓[/green] Selected: {result}")

        else:  # Custom input
            result = Prompt.ask("\n[bold]Enter custom subsector[/bold]")
            self.console.print(f"[green]✓[/green] Custom subsector: {result}")

        # Track correction
        if suggestions:
            self._track_correction(
                "subsector", top_suggestion, result,
                document_summary, suggestions[0][1]
            )

        self.console.print()
        return result

    def ask_document_type(self, suggestions: List[Tuple[str, float]]) -> str:
        """Ask user to select document type.

        Args:
            suggestions: List of (document_type, confidence) tuples

        Returns:
            User-selected document type
        """
        self.console.clear()
        self.console.print(Panel(
            "[bold magenta]Document Type Classification[/bold magenta]",
            border_style="magenta",
            box=box.DOUBLE
        ))
        self.console.print()

        # Show AI suggestions
        if suggestions:
            self._show_suggestions(suggestions, "AI Suggested Document Types")

        # Ask user decision
        self.console.print("[bold]What would you like to do?[/bold]")
        if suggestions:
            self.console.print("1. Accept top AI suggestion")
            self.console.print("2. Choose from all document types")
            self.console.print("3. Enter custom document type")
            choices = ["1", "2", "3"]
        else:
            self.console.print("1. Choose from all document types")
            self.console.print("2. Enter custom document type")
            choices = ["1", "2"]

        self.console.print()

        choice = Prompt.ask(
            "Your choice",
            choices=choices,
            default="1"
        )

        result = None
        top_suggestion = suggestions[0][0] if suggestions else None

        if suggestions and choice == "1":
            result = top_suggestion
            self.console.print(f"[green]✓[/green] Accepted: {result}")

        elif (suggestions and choice == "2") or (not suggestions and choice == "1"):
            self.console.print()
            self._show_options_menu(self.DOCUMENT_TYPES, "Document Types")

            type_choice = Prompt.ask(
                "Select document type number",
                choices=[str(i) for i in range(1, len(self.DOCUMENT_TYPES) + 1)]
            )
            result = self.DOCUMENT_TYPES[int(type_choice) - 1]
            self.console.print(f"[green]✓[/green] Selected: {result}")

        else:  # Custom input
            result = Prompt.ask("\n[bold]Enter custom document type[/bold]")
            self.console.print(f"[green]✓[/green] Custom document type: {result}")

        # Track correction
        if suggestions:
            self._track_correction(
                "document_type", top_suggestion, result,
                "", suggestions[0][1]
            )

        self.console.print()
        return result

    def batch_classify(self, documents: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Batch classify multiple documents with user interaction.

        Args:
            documents: List of document dicts with keys:
                - summary: Document content
                - suggested_sector: AI suggestion
                - sector_confidence: AI confidence
                - subsector_suggestions: List of (subsector, confidence)
                - type_suggestions: List of (doc_type, confidence)

        Returns:
            List of classification dicts with keys:
                - sector: User-selected sector
                - subsector: User-selected subsector
                - document_type: User-selected document type
        """
        results = []
        total = len(documents)

        self.console.print(Panel(
            f"[bold cyan]Batch Classification: {total} documents[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        ))
        self.console.print()

        for idx, doc in enumerate(documents, 1):
            self.console.print(f"\n[bold]Document {idx}/{total}[/bold]")
            self.console.print("─" * 60)

            # Ask for sector
            sector = self.ask_sector_classification(
                doc["summary"],
                doc["suggested_sector"],
                doc["sector_confidence"]
            )

            # Ask for subsector
            subsector = self.ask_subsector_classification(
                sector,
                doc["summary"],
                doc.get("subsector_suggestions", [])
            )

            # Ask for document type
            doc_type = self.ask_document_type(
                doc.get("type_suggestions", [])
            )

            results.append({
                "sector": sector,
                "subsector": subsector,
                "document_type": doc_type
            })

            # Show progress
            self.console.print(f"\n[green]✓[/green] Classified {idx}/{total} documents")

            if idx < total:
                continue_batch = Confirm.ask(
                    "\nContinue to next document?",
                    default=True
                )
                if not continue_batch:
                    self.console.print("[yellow]Batch classification stopped by user[/yellow]")
                    break

        # Summary
        self.console.print("\n" + "═" * 60)
        self.console.print(Panel(
            f"[bold green]Batch Classification Complete![/bold green]\n"
            f"Classified: {len(results)}/{total} documents",
            border_style="green",
            box=box.DOUBLE
        ))

        return results

    def get_correction_stats(self) -> Dict[str, Any]:
        """Get statistics about user corrections.

        Returns:
            Dictionary with correction statistics
        """
        if not self.qdrant_client:
            return {"error": "No Qdrant client configured"}

        try:
            # Scroll through all corrections
            corrections = []
            offset = None

            while True:
                response = self.qdrant_client.scroll(
                    collection_name=self.collection_name,
                    limit=100,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False
                )

                if not response[0]:
                    break

                corrections.extend(response[0])
                offset = response[1]

                if offset is None:
                    break

            # Calculate statistics
            total = len(corrections)
            corrected = sum(1 for c in corrections if c.payload.get("was_corrected", False))

            by_type = {}
            for correction in corrections:
                ctype = correction.payload.get("correction_type", "unknown")
                if ctype not in by_type:
                    by_type[ctype] = {"total": 0, "corrected": 0}
                by_type[ctype]["total"] += 1
                if correction.payload.get("was_corrected", False):
                    by_type[ctype]["corrected"] += 1

            return {
                "total_interactions": total,
                "total_corrections": corrected,
                "correction_rate": corrected / total if total > 0 else 0,
                "by_type": by_type
            }

        except Exception as e:
            return {"error": str(e)}
