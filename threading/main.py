from threading_medical_device_processor import*


def run_with_threads(analyzer):
    start = time.time()
    tasks = [
        analyzer.save_warranty_report,
        analyzer.save_problem_clinics,
        analyzer.save_calibration_report,
        analyzer.save_pivot_table
    ]
    threads = []
    for task in tasks:
        t = threading.Thread(target=task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    return time.time() - start


async def run_with_asyncio(analyzer):
    start = time.time()
    loop = asyncio.get_event_loop()
    # Pandas блокирует поток, поэтому запускаем в экзекуторе
    tasks = [
        loop.run_in_executor(None, analyzer.save_warranty_report),
        loop.run_in_executor(None, analyzer.save_problem_clinics),
        loop.run_in_executor(None, analyzer.save_calibration_report),
        loop.run_in_executor(None, analyzer.save_pivot_table)
    ]
    await asyncio.gather(*tasks)
    return time.time() - start


def main():
    # Загрузка и подготовка (как в твоем старом main.py)
    raw_df = pd.read_excel('medical_diagnostic_devices_10000.xlsx')
    normalizer = StatusNormalizer()
    raw_df['status'] = raw_df['status'].apply(normalizer.normalize)

    analyzer = ThreadedDeviceAnalyzer(raw_df)
    analyzer.normalize_dates()

    # Замеры
    t_time = run_with_threads(analyzer)
    a_time = asyncio.run(run_with_asyncio(analyzer))

    print(f"\n--- Результаты ---")
    print(f"Threading time: {t_time:.4f}s")
    print(f"Asyncio time:   {a_time:.4f}s")


if __name__ == "__main__":
    main()