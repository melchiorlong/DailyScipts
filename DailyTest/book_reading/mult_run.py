from multiprocessing import Process
from book_reading_word import BookReadingWord
# from name_list import name_dict


def run_reading(real_name, job_number):
	app = BookReadingWord(
		real_name=real_name,
		job_number=job_number,
	)
	app.run()


if __name__ == '__main__':

	name_dict = {
		# '吕正阳': '22081988',
		# '曲世林': '22061886',
		'田龙': '22092063',
	}

	for name, number in name_dict.items():
		p = Process(target=run_reading, args=(name, number))
		p.start()
