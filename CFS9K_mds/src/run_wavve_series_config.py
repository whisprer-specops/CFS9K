from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

scheduler.add_job(lambda: run_wave_series(cfg), 'interval', minutes=60)
scheduler.start()