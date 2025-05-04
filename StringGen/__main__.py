import asyncio
import importlib
import logging
from pyrogram import idle
from StringGen import LOGGER, Anony
from StringGen.modules import ALL_MODULES

async def safe_import(module_name):
    """Safely import a module"""
    try:
        importlib.import_module(f"StringGen.modules.{module_name}")
        LOGGER.info(f"Successfully imported {module_name}")
        return True
    except Exception as e:
        LOGGER.error(f"Failed to import {module_name}: {str(e)}")
        return False

async def handle_flood_wait(error_msg):
    """Handle flood wait errors"""
    try:
        wait_time = int(''.join(filter(str.isdigit, error_msg.split("FLOOD_WAIT_")[1].split()[0])))
        LOGGER.warning(f"Flood wait detected. Waiting {wait_time} seconds...")
        await asyncio.sleep(wait_time + 5)
        return wait_time
    except (IndexError, ValueError) as e:
        LOGGER.error(f"Could not parse flood wait time: {error_msg}")
        return None

async def anony_boot():
    """Main bot startup function"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            await Anony.start()
            LOGGER.info("Connected to Telegram API")
            break
        except Exception as ex:
            error_msg = str(ex)
            
            if "FLOOD_WAIT" in error_msg:
                wait_time = await handle_flood_wait(error_msg)
                if wait_time is None and attempt == max_retries - 1:
                    LOGGER.critical("Max retries reached. Exiting...")
                    return
            else:
                LOGGER.error(f"Connection error: {error_msg}")
                if attempt == max_retries - 1:
                    LOGGER.critical("Max retries reached. Exiting...")
                    return
                await asyncio.sleep(5)

    # Import all modules
    successful_imports = 0
    for module in ALL_MODULES:
        if await safe_import(module):
            successful_imports += 1

    LOGGER.info(f"Loaded {successful_imports}/{len(ALL_MODULES)} modules")
    LOGGER.info(f"Bot @{Anony.username} is running!")
    
    # Keep the bot running
    await idle()

    # Cleanup when idle ends
    try:
        if Anony.is_connected:
            await Anony.stop()
            LOGGER.info("Bot stopped gracefully")
    except Exception as e:
        LOGGER.error(f"Error while stopping bot: {str(e)}")

async def main():
    """Entry point with proper error handling"""
    try:
        await anony_boot()
    except KeyboardInterrupt:
        LOGGER.warning("Received keyboard interrupt...")
    except Exception as e:
        LOGGER.critical(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        LOGGER.info("Bot shutdown complete")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
