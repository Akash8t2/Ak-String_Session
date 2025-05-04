import asyncio
import importlib
import time
from pyrogram import idle
from StringGen import LOGGER, Anony
from StringGen.modules import ALL_MODULES

async def safe_import(module_name):
    try:
        importlib.import_module(f"StringGen.modules.{module_name}")
        LOGGER.info(f"Successfully imported {module_name}")
        return True
    except Exception as e:
        LOGGER.error(f"Failed to import {module_name}: {str(e)}")
        return False

async def anony_boot():
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            await Anony.start()
            break
        except Exception as ex:
            if "FLOOD_WAIT" in str(ex):
                wait_time = int(str(ex).split()[-2])
                LOGGER.warning(f"Flood wait detected. Waiting for {wait_time} seconds...")
                time.sleep(wait_time + retry_delay)
            else:
                LOGGER.error(f"Startup failed: {str(ex)}")
                if attempt == max_retries - 1:
                    quit(1)
                time.sleep(retry_delay)

    # मॉड्यूल्स इम्पोर्ट करें
    successful_imports = 0
    for module in ALL_MODULES:
        if await safe_import(module):
            successful_imports += 1

    LOGGER.info(f"Successfully imported {successful_imports}/{len(ALL_MODULES)} modules")
    LOGGER.info(f"Bot @{Anony.username} is now running!")
    
    await idle()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(anony_boot())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        LOGGER.error(f"Fatal error: {str(e)}")
    finally:
        LOGGER.info("Bot has stopped.")
