"""Implementation of a Volumio inteface."""
import aiohttp
import asyncio
import urllib

class Volumio:
    """A connection to Volumio."""

    def __init__(self, host, port, session=None):
        """Initialize the object."""
        self._host = host
        self._port = port
        self._created_session = False
        self._session = session
    
    def _init_session(self):
        if self._session == None:
            self._session = aiohttp.ClientSession()
            self._created_session = True

    async def close(self):
        """Close the connection."""
        if self._created_session and self._session is not None:
            await self._session.close()
            self._session = None
            self._created_session = False

    async def _send_volumio_msg(self, method, params=None):
        url = f"http://{self._host}:{self._port}/api/v1/{method}/"

        try:
            self._init_session()
            response = await self._session.get(url, params=params)
            if response.status == 200:
                return await response.json()
            else:
                raise CannotConnectError(response)
        except aiohttp.client_exceptions.ContentTypeError:
            # hack to handle methods not supported by older versions
            return {}
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            raise CannotConnectError() from error

    async def get_system_version(self):
        """Get the systems version."""
        response = await self._send_volumio_msg("getSystemVersion")
        return response.copy()

    async def get_system_info(self):
        """Get the systems information."""
        response = await self._send_volumio_msg("getSystemInfo")
        return response.copy()

    async def get_state(self):
        """Get the Volumio state."""
        response = await self._send_volumio_msg("getState")
        return response.copy()

    async def get_playlists(self):
        """Get available Volumio playlists."""
        response = await self._send_volumio_msg("listplaylists")
        return response.copy()

    async def next(self):
        """Send 'next' command to Volumio."""
        await self._send_volumio_msg("commands", params={"cmd": "next"})

    async def previous(self):
        """Send 'previous' command to Volumio."""
        await self._send_volumio_msg("commands", params={"cmd": "prev"})

    async def play(self):
        """Send 'play' command to Volumio."""
        await self._send_volumio_msg("commands", params={"cmd": "play"})

    async def pause(self):
        """Send 'pause' command to Volumio."""
        await self._send_volumio_msg("commands", params={"cmd": "pause"})

    async def stop(self):
        """Send 'stop' command to Volumio."""
        await self._send_volumio_msg("commands", params={"cmd": "stop"})

    async def set_volume_level(self, volume):
        """Send volume level to Volumio."""
        await self._send_volumio_msg(
            "commands", params={"cmd": "volume", "volume": volume}
        )

    async def volume_up(self):
        """Send 'volume up' command to Volumio."""
        await self._send_volumio_msg(
            "commands", params={"cmd": "volume", "volume": "plus"}
        )

    async def volume_down(self):
        """Send 'volume down' command to Volumio."""
        await self._send_volumio_msg(
            "commands", params={"cmd": "volume", "volume": "minus"}
        )

    async def mute(self):
        """Send 'mute' command to Volumio."""
        await self._send_volumio_msg(
            "commands", params={"cmd": "volume", "volume": "mute"}
        )

    async def unmute(self):
        """Send 'unmute' command to Volumio."""
        await self._send_volumio_msg(
            "commands", params={"cmd": "volume", "volume": "unmute"}
        )

    async def set_shuffle(self, shuffle):
        """Enable/disable shuffle mode."""
        await self._send_volumio_msg(
            "commands", params={"cmd": "random", "value": str(shuffle).lower()}
        )

    async def play_playlist(self, playlist):
        """Choose an available playlist and play it."""
        await self._send_volumio_msg(
            "commands", params={"cmd": "playplaylist", "name": playlist}
        )

    async def clear_playlist(self):
        """Clear current playlist."""
        await self._send_volumio_msg("commands", params={"cmd": "clearQueue"})

    def canonic_url(self, url):
        """Creates a full url from a potentially relative one."""
        if url is None:
            return
        if str(url[0:2]).lower() == "ht":
            return url
        return urllib.parse.urljoin(f"http://{self._host}:{self._port}", url)


class CannotConnectError(Exception):
    """Exception to indicate an error in connection."""
