"""
Tests pour le module ExifParser

Ce module teste le parsing des données EXIF des images.
"""
import io
from pathlib import Path

import pytest

from libs.exif_parser import ExifParser


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def iphone_image_path() -> Path:
    """
    Fixture : Chemin vers ta photo iPhone.

    Cette fixture retourne le chemin absolu vers l'image de test.

    Returns:
        Path: Chemin vers le fichier image.
    """
    fixtures_dir = Path(__file__).parent / "fixtures"
    image_path = fixtures_dir / "visage.jpg"
    if not image_path.exists():
        pytest.fail(
            f"Image de test non trouvée : {image_path}\n"
            f"Copie une photo iPhone dans ce dossier : {fixtures_dir}"
        )

    return image_path


@pytest.fixture
def iphone_image_bytes(iphone_image_path: Path) -> io.BytesIO:
    """
    Fixture : Ta photo iPhone en format BytesIO.

    Cette fixture lit le fichier image et le convertit en flux binaire
    pour simuler un upload HTTP (comme ce que recevra l'API).

    Args:
        iphone_image_path: Chemin vers l'image (de la fixture précédente).

    Returns:
        io.BytesIO: Flux binaire de l'image.
    """
    with open(iphone_image_path, "rb") as image_file:
        image_bytes = io.BytesIO(image_file.read())

    return image_bytes


@pytest.fixture
def parsed_exif_parser(iphone_image_bytes: io.BytesIO) -> ExifParser:
    """
    Fixture : Parser EXIF déjà initialisé et parsé.

    Cette fixture crée un parser et appelle parse() pour toi.
    Utile pour éviter de répéter ce code dans chaque test.

    Args:
        iphone_image_bytes: Image en BytesIO (de la fixture précédente).

    Returns:
        ExifParser: Parser prêt à utiliser.
    """
    parser = ExifParser(iphone_image_bytes)
    parser.parse()
    return parser


# =============================================================================
# TESTS
# =============================================================================

class TestExifParserInitialization:
    """Tests pour l'initialisation du parser EXIF."""

    def test_parser_initializes_with_bytesio(self, iphone_image_bytes):
        """
        Le parser doit s'initialiser avec un objet BytesIO.

        Ce test vérifie que :
        1. On peut créer une instance de ExifParser
        2. L'objet est bien de type ExifParser
        """
        # Arrange (Préparation)
        # → La fixture iphone_image_bytes prépare l'image

        # Act (Action)
        parser = ExifParser(iphone_image_bytes)

        # Assert (Vérification)
        assert isinstance(parser, ExifParser)
        assert parser.parsed_exif == {}  # Doit être vide avant parse()


class TestExifParserParse:
    """Tests pour la méthode parse() du parser EXIF."""

    def test_parse_returns_true_for_iphone_image(self, iphone_image_bytes):
        """
        La méthode parse() doit retourner True pour une image iPhone valide.

        Ce test vérifie que :
        1. parse() retourne True (succès)
        2. Aucune exception n'est levée
        """
        # Arrange
        parser = ExifParser(iphone_image_bytes)

        # Act
        result = parser.parse()

        # Assert
        assert result is True

    def test_parse_populates_parsed_exif(self, parsed_exif_parser):
        """
        La méthode parse() doit remplir le dictionnaire parsed_exif.

        Ce test vérifie que :
        1. parsed_exif n'est plus vide après parse()
        2. Il contient des données EXIF
        """
        # Arrange
        # → La fixture parsed_exif_parser a déjà appelé parse()

        # Act
        exif_data = parsed_exif_parser.parsed_exif

        # Assert
        assert isinstance(exif_data, dict)
        assert len(exif_data) > 0  # Doit contenir des données

    def test_has_exif_returns_true(self, parsed_exif_parser):
        """
        has_exif() doit retourner True pour une photo iPhone.

        Les photos iPhone contiennent toujours des metadata EXIF.
        """
        # Act
        result = parsed_exif_parser.has_exif()

        # Assert
        assert result is True


class TestExifParserGetters:
    """Tests pour les méthodes getter du parser EXIF."""

    def test_get_camera_make_is_apple(self, parsed_exif_parser):
        """
        get_camera_make() doit retourner 'Apple' pour une photo iPhone.
        """
        # Act
        camera_make = parsed_exif_parser.get_camera_make()

        # Assert
        assert camera_make == "Apple"

    def test_get_camera_model_contains_iphone(self, parsed_exif_parser):
        """
        get_camera_model() doit contenir 'iPhone' pour une photo iPhone.
        """
        # Act
        camera_model = parsed_exif_parser.get_camera_model()

        # Assert
        assert camera_model is not None
        assert "iPhone" in camera_model

    def test_get_software_exists(self, parsed_exif_parser):
        """
        get_software() doit retourner un logiciel (ex: iOS).
        """
        # Act
        software = parsed_exif_parser.get_software()

        # Assert
        assert software is not None
        assert len(software) > 0

    def test_get_summary_returns_all_metadata(self, parsed_exif_parser):
        """
        get_summary() doit retourner un résumé complet des metadata.
        """
        # Act
        summary = parsed_exif_parser.get_summary()

        # Assert
        assert isinstance(summary, dict)
        assert "has_exif" in summary
        assert "make" in summary
        assert "model" in summary
        assert "software" in summary
        assert summary["has_exif"] is True
        assert summary["make"] == "Apple"

