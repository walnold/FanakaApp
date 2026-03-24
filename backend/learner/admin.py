from django.contrib import admin
from learner.models.learner import Learner, LearnerStatus
from learner.models.enrollement import Enrollement, EnrollementStatus
from learner.models.lessons import Lesson
from learner.models.payments import Payments

# Register your models here.
admin.site.register(Learner)
admin.site.register(LearnerStatus)
admin.site.register(Enrollement)
admin.site.register(EnrollementStatus)
admin.site.register(Lesson)
admin.site.register(Payments)