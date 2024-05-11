import reflex as rx
import base64

import boto3
import io
from PIL import Image, ImageDraw, ImageFont

rekognition_client = boto3.client("rekognition")


class State(rx.State):
    """The app state."""

    img: str = ""

    @staticmethod
    def recognize(image: rx.UploadFile):
        try:
            image_bytes = image.file.read()

            response = rekognition_client.detect_labels(Image={"Bytes": image_bytes})

            image = Image.open(io.BytesIO(image_bytes))

            font = ImageFont.truetype("dev/fonts/arial.ttf", size=32)

            draw = ImageDraw.Draw(image)

            width, height = image.size

            for label in response["Labels"]:
                name = label["Name"]

                for instance in label["Instances"]:
                    bounding_box = instance["BoundingBox"]

                    x0 = int(bounding_box["Left"] * width)
                    y0 = int(bounding_box["Top"] * height)
                    x1 = x0 + int(bounding_box["Width"] * width)
                    y1 = y0 + int(bounding_box["Height"] * height)

                    draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=10)
                    draw.text((x0, y1), name, font=font, fill=(255, 0, 0))

            with io.BytesIO() as output:
                image.save(output, format="PNG")
                image_base64 = base64.b64encode(output.getvalue()).decode("utf-8")

            return image_base64
        except Exception as e:
            print(e)

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of a file to recognise.

        Args:
            file: The uploaded file.
        """
        for file in files:
            image = self.recognize(file)

            self.img = image


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Recognize", size="9", font_family="Share Tech Mono"),
            rx.text("Get started by uploading a file"),
            rx.upload(
                rx.button(
                    "Select file",
                    size="4",
                ),
                id="upload",
                multiple=False,
                accept={
                    "image/png": [".png"],
                    "image/jpeg": [".jpg", ".jpeg"],
                    "image/webp": [".webp"],
                },
                max_files=1,
                disabled=False,
                on_keyboard=True,
                on_drop=State.handle_upload(rx.upload_files(upload_id="upload")),
            ),
            rx.cond(
                State.img != "",
                rx.image(src=f"data:image/png;base64,{State.img}"),
                rx.text(""),
            ),
            align="center",
            spacing="4",
            font_size="2em",
        ),
        height="100vh",
        font_family="Share Tech Mono",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@700&family=Share+Tech+Mono&display=swap"
    ]
)

app.add_page(index)
