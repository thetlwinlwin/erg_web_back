import io

from fastapi import HTTPException
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest, MediaIoBaseDownload

from .mime_types import GoogleMimeTypes as Mime


class GoogleDrive:
    def __init__(self, service) -> None:
        self._files = service.files()

    def get_docs(self, folder_id: str = None) -> list[str]:
        return self._search(
            mime_types=[
                Mime.doc,
            ],
            id=folder_id,
        )

    def get_folders(self) -> list[str]:
        results = self._search(
            mime_types=[
                Mime.folder,
            ],
        )
        for folder in results:
            if folder.get("name") == "Events":
                results.remove(folder)
                break

        return results

    def get_images(self, folder_id: str) -> list[str]:
        return self._search(
            id=folder_id,
            mime_types=[
                Mime.jpg,
                Mime.png,
            ],
        )

    def _search(
        self,
        mime_types: list[Mime],
        id: str = None,
    ) -> list[str]:
        try:
            results = []
            page_token = None

            def _converter(txt: Mime):
                return f"mimeType='{txt.value}'"

            mime_types = list(map(_converter, mime_types))
            mime_str = " or ".join(mime_types)

            while True:
                q = f"'{id}' in parents and {mime_str}"
                if id == None:
                    q = mime_str
                response = self._files.list(
                    q=q,
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                ).execute()
                results.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)

                if page_token is None:
                    break
            return results
        except HttpError as error:
            raise HTTPException(
                status_code=error.status_code,
                detail=error.reason,
            )

    def refresh(self) -> dict:
        events = dict()
        folders = self.get_folders()
        for folder in folders:
            id = folder.get("id")
            name = folder.get("name")
            file_list = self.get_docs(folder_id=id)
            if file_list:
                details = self._read_doc(
                    id=file_list[0].get("id"),
                )
            events[name] = {
                "name": name,
                "id": id,
                **details,
                "file_info": file_list[0] if file_list else None,
                "img_links": self.get_images(folder_id=id),
            }
        return events

    def _read_doc(self, id: str = None) -> dict:
        res = self._download(id)
        res_txt = res.decode(encoding="utf-8-sig")
        txt_list = res_txt.split("\n")
        result = dict()
        for txt in txt_list:
            txt_result = txt.split("-")
            # match txt_result:
            #     case ["title" | "Title" | "TITLE", val]:
            #         result["title"] = val.strip().title()
            #     case ["date" | "Date" | "DATE", val]:
            #         result["date"] = val.strip()
            #     case [
            #         "content"
            #         | "Content"
            #         | "CONTENT"
            #         | "description"
            #         | "Description"
            #         | "DESCRIPTION"
            #         | "contents"
            #         | "Contents"
            #         | "CONTENTS"
            #         | "descriptions"
            #         | "Descriptions"
            #         | "DESCRIPTIONS",
            #         val,
            #     ]:
            #         result["description"] = val.strip().capitalize()
            if txt_result[0] in ["title", "Title", "TITLE"]:
                result["title"] = txt_result[1].strip().title()
            elif txt_result[0] in ["date", "Date", "DATE"]:
                result["date"] = txt_result[1].strip()
            elif txt_result[0] in [
                "content",
                "Content",
                "CONTENT",
                "description",
                "Description",
                "DESCRIPTION",
                "contents",
                "Contents",
                "CONTENTS",
                "descriptions",
                "Descriptions",
                "DESCRIPTIONS",
            ]:
                result["description"] = txt_result[1].strip().capitalize()

        return result

    def _download(
        self,
        id: str,
        mimeType: Mime = Mime.text,
    ) -> bytes:
        file = io.BytesIO()
        req: HttpRequest = self._files.export_media(
            fileId=id,
            mimeType=mimeType.value,
        )
        try:
            downloader = MediaIoBaseDownload(file, req)
            done = False
            while done is False:
                _, done = downloader.next_chunk()
        except HttpError as error:
            file = None
            raise HTTPException(
                status_code=error.status_code,
                detail=error.reason,
            )
        return file.getvalue()
