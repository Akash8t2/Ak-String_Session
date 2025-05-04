import asyncio
import importlib
import logging
from pyrogram import idle
from StringGen import LOGGER, Anony
from StringGen.modules import ALL_MODULES

async def safe_import(module_name):
    """सुरक्षित तरीके से मॉड्यूल इम्पोर्ट करने के लिए फंक्शन"""
    try:
        importlib.import_module(f"StringGen.modules.{module_name}")
        LOGGER.info(f"{module_name} मॉड्यूल सफलतापूर्वक इम्पोर्ट हुआ")
        return True
    except Exception as e:
        LOGGER.error(f"{module_name} मॉड्यूल इम्पोर्ट करने में असफल: {str(e)}")
        return False

async def handle_flood_wait(error_msg):
    """Flood wait एरर को हैंडल करने के लिए फंक्शन"""
    try:
        # 'FLOOD_WAIT_X' से वेट टाइम निकालें (X सेकंड्स)
        wait_time = int(''.join(filter(str.isdigit, error_msg.split("FLOOD_WAIT_")[1].split()[0])))
        LOGGER.warning(f"Telegram ने फ्लड वेट दिया: {wait_time} सेकंड्स...")
        await asyncio.sleep(wait_time + 5)  # 5 सेकंड एक्स्ट्रा बफर
        return wait_time
    except (IndexError, ValueError) as e:
        LOGGER.error(f"फ्लड वेट टाइम पार्स नहीं कर पाया: {error_msg}")
        return None

async def anony_boot():
    """बॉट स्टार्ट करने की मेन फंक्शन"""
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            await Anony.start()
            LOGGER.info("बॉट टेलीग्राम API से कनेक्ट हुआ")
            break
        except Exception as ex:
            error_msg = str(ex)
            
            if "FLOOD_WAIT" in error_msg:
                wait_time = await handle_flood_wait(error_msg)
                if wait_time is None:
                    continue
            else:
                LOGGER.error(f"कनेक्शन एरर: {error_msg}")
                if attempt == max_retries - 1:
                    LOGGER.critical("मैक्सिमम रिट्री हुई. बॉट बंद हो रहा है...")
                    quit(1)
                await asyncio.sleep(retry_delay)

    # सभी मॉड्यूल्स इम्पोर्ट करें
    successful_imports = 0
    for module in ALL_MODULES:
        if await safe_import(module):
            successful_imports += 1

    LOGGER.info(f"{successful_imports}/{len(ALL_MODULES)} मॉड्यूल्स सफलतापूर्वक लोड हुए")
    LOGGER.info(f"बॉट @{Anony.username} चल रहा है!")
    
    # बॉट को इडल स्टेट में रखें
    await idle()

if __name__ == "__main__":
    try:
        # इवेंट लूप शुरू करें
        loop = asyncio.get_event_loop()
        loop.run_until_complete(anony_boot())
    except KeyboardInterrupt:
        LOGGER.warning("कीबोर्ड इंटरप्ट मिला...")
    except Exception as e:
        LOGGER.critical(f"गंभीर त्रुटि: {str(e)}", exc_info=True)
    finally:
        LOGGER.info("बॉट बंद हो रहा है...")
        # सभी रिसोर्सेज क्लीन अप करें
        try:
            if Anony.is_connected:
                await Anony.stop()
        except Exception:
            pass
