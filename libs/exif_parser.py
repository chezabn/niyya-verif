"""
Parser EXIF générique pour Niyya Verify.

Ce module fournit des utilitaires pour extraire et analyser
les données EXIF des images JPEG.

Example:
    >>> from io import BytesIO
    >>> from libs.exif_parser import ExifParser
    >>> image_data = BytesIO(open("photo.jpg", "rb").read())
    >>> parser = ExifParser(image_data)
    >>> parser.parse()
    >>> print(parser.get_camera_model())
    'iPhone 14 Pro'
"""

from io import BytesIO
from typing import Any, Dict, Optional

from PIL import Image
from PIL.ExifTags import TAGS


class ExifParserError(Exception):
    """Exception levée lors d'une erreur de parsing EXIF."""

    pass


class ExifParser:
    """
    Parseur de données EXIF pour les images.

    Ce classe fournit des méthodes pour extraire, parser et
    analyser les metadata EXIF des images JPEG.

    Attributes:
        image_data: Flux binaire de l'image (BytesIO).
        image: Instance PIL Image ouverte.
        parsed_exif: Dictionnaire des données EXIF parsées.

    Example:
        >>> from io import BytesIO
        >>> from libs.exif_parser import ExifParser
        >>> image_data = BytesIO(open("photo.jpg", "rb").read())
        >>> parser = ExifParser(image_data)
        >>> parser.parse()
        >>> print(parser.get_camera_model())
        'iPhone 14 Pro'
    """

    def __init__(self, image_data: BytesIO) -> None:
        """
        Initialise le parseur EXIF.

        Args:
            image_data: Flux binaire de l'image (BytesIO).
        """
        self.image_data = image_data
        self.image: Optional[Image.Image] = None
        self.parsed_exif: Dict[str, Any] = {}

    def parse(self) -> bool:
        """
        Parse les données EXIF de l'image.

        Returns:
            bool: True si les données EXIF ont été parsées avec succès.

        Raises:
            ExifParserError: Si l'image est invalide ou corrompue.
        """
        try:
            # Reset le flux pour lecture
            self.image_data.seek(0)

            # Ouvrir et vérifier l'image
            self.image = Image.open(self.image_data)
            self.image.verify()

            # Réouvrir car verify() corrompt l'objet
            self.image_data.seek(0)
            self.image = Image.open(self.image_data).convert("RGB")

            # Extraire les données EXIF
            exif_data = self.image.getexif()

            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    self.parsed_exif[tag] = value

            return True

        except Exception as exception:
            raise ExifParserError(
                f"Erreur lors du parsing EXIF: {exception}"
            ) from exception

    def has_exif(self) -> bool:
        """
        Vérifie si l'image contient des données EXIF.

        Returns:
            bool: True si des données EXIF sont présentes.
        """
        return bool(self.parsed_exif)

    def get_tag(self, tag_name: str, default: Any = None) -> Any:
        """
        Récupère la valeur d'un tag EXIF spécifique.

        Args:
            tag_name: Nom du tag EXIF (ex: 'Make', 'Model').
            default: Valeur par défaut si le tag n'existe pas.

        Returns:
            Any: Valeur du tag ou default.
        """
        return self.parsed_exif.get(tag_name, default)

    def get_camera_make(self) -> Optional[str]:
        """
        Récupère la marque de la caméra.

        Returns:
            Optional[str]: Marque de la caméra ou None.
        """
        return self.get_tag("Make")

    def get_camera_model(self) -> Optional[str]:
        """
        Récupère le modèle de la caméra.

        Returns:
            Optional[str]: Modèle de la caméra ou None.
        """
        return self.get_tag("Model")

    def get_datetime(self) -> Optional[str]:
        """
        Récupère la date et heure de capture.

        Returns:
            Optional[str]: Date/heure de capture ou None.
        """
        return self.get_tag("DateTime")

    def get_software(self) -> Optional[str]:
        """
        Récupère le logiciel utilisé pour la capture.

        Returns:
            Optional[str]: Logiciel utilisé ou None.
        """
        return self.get_tag("Software")

    def get_all_tags(self) -> Dict[str, Any]:
        """
        Récupère tous les tags EXIF parsés.

        Returns:
            Dict[str, Any]: Dictionnaire complet des tags EXIF.
        """
        return self.parsed_exif.copy()

    def get_summary(self) -> Dict[str, Any]:
        """
        Récupère un résumé des metadata importantes.

        Returns:
            Dict[str, Any]: Résumé des metadata clés.
        """
        return {
            "has_exif": self.has_exif(),
            "make": self.get_camera_make(),
            "model": self.get_camera_model(),
            "datetime": self.get_datetime(),
            "software": self.get_software(),
            "total_tags": len(self.parsed_exif),
        }
